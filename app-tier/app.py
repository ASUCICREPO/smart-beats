import threading
from zipfile import ZipFile

from flask import Flask, request

import uuid
import sys
import subprocess
import settings as s
import utils as u
import boto3
import os.path

logger = u.init_logger(__name__)
app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    file_name = None
    script_params = {}
    try:
        request_params = dict(request.form)
        logger.info(f'Request params received from web server: {request_params}')

        script_params = get_beat_generator_params(request_params)
        logger.info(f'Script params: {script_params}')

        params_as_script_argument = "<param>".join([f"{k}<=>{v}" for k, v in script_params.items()])
        logger.info(f'Script params in concatenated format: {params_as_script_argument}')

        proc = subprocess.run([sys.executable, 'beat_generator.py', params_as_script_argument])
        logger.info(f'Subprocess return code: {proc.returncode}')

        response_txt = None
        if proc.returncode == 0:
            logger.info('Script executed successfully. Creating zip file')
            zip_path, file_name = create_output_zip_file(script_params[s.beat_name])

            logger.info(f'Uploading zip file to S3: {file_name}')
            upload_file_to_s3(zip_path, file_name)
            response_txt = file_name
        else:
            logger.error(f"Beat generation script exited with non-zero status: {proc.returncode}")
            return f"App server has encountered an unexpected condition", 500

        if not response_txt:
            logger.error(f"Couldn't create zip file: {file_name}")
            return f"There was an issue processing your request", 400

        return response_txt, 200

    finally:
        if s.input_shapefile_path in script_params:
            pwcc_file_name = script_params[s.input_shapefile_path].split('.')[0]
            logger.info(f'pwcc file path to be deleted: {pwcc_file_name}')
            t1 = threading.Thread(target=u.delete_file, args=(pwcc_file_name,))
            t1.start()

        if file_name:
            output_file_name = f"{s.output_path}/{file_name.split('.')[0]}"
            logger.info(f'Output file path to be deleted: {output_file_name}')
            t2 = threading.Thread(target=u.delete_file, args=(output_file_name,))
            t2.start()


def get_beat_generator_params(request_params):
    params = {}

    # Unique Beat name
    beat_name = ''.join([str(uuid.uuid4().hex[:6]), '_beat'])
    params[s.beat_name] = beat_name

    # Polygon-wise crime count shapefile location
    pwcc_shapefile_name = request_params['polygon_wise_count_shapefile']
    u.download_file_from_s3(s.output_s3_bucket_name, pwcc_shapefile_name)
    pwcc_shapefile_prefix = pwcc_shapefile_name.split('.')[0]
    params[s.input_shapefile_path] = f'data/input/{pwcc_shapefile_prefix}.shp'

    # Build balanced zones params
    params[s.zone_creation_method] = request_params[s.beat_creation_method]

    if params[s.zone_creation_method] == 'ATTRIBUTE_TARGET':
        params[s.zone_building_criteria_target] = f"count {request_params.get('cfs_per_beat', 10000)} 1"
    elif params[s.zone_creation_method] == 'NUMBER_ZONES_AND_ATTRIBUTE':
        params[s.number_of_zones] = request_params[s.number_of_beats]
        params[s.zone_building_criteria] = "count 1"

    return params


def create_output_zip_file(beat_name):
    with ZipFile(f'{s.output_path}/{beat_name}.zip', 'w') as zip_obj:
        for ext in s.shapefile_components:
            file_path = f'{s.output_path}/{beat_name}{ext}'
            if os.path.exists(file_path):
                logger.info(file_path + " : EXISTS")
                zip_obj.write(f'{s.output_path}/{beat_name}{ext}', f'{beat_name}{ext}')
            else:
                logger.info(file_path + " : DOESN'T EXIST")

    return f'{s.output_path}/{beat_name}.zip', f'{beat_name}.zip'


def upload_file_to_s3(filepath, object_name):
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(s.output_s3_bucket_name).upload_file(filepath, f'{s.s3_beats_dir_name}/{object_name}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
