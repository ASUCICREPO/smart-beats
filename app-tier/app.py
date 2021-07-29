from zipfile import ZipFile

from flask import Flask, request
from utils import init_logger

import uuid
import sys
import subprocess
import settings as s
import boto3

logger = init_logger(__name__)
app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
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


def get_beat_generator_params(request_params):
    params = {}

    # Unique Beat name
    beat_name = ''.join([str(uuid.uuid4().hex[:6]), '_beat'])
    params[s.beat_name] = beat_name

    # Polygon-wise crime count shapefile location
    params[s.input_shapefile_path] = 'data/input2/census_wise_crime_counts.shp'

    # Build balanced zones params
    params[s.zone_creation_method] = request_params[s.beat_creation_method]

    if params[s.zone_creation_method] == 'ATTRIBUTE_TARGET':
        params[s.zone_building_criteria_target] = f"count {request_params.get('cfs_per_beat', 10000)} 1"
    elif params[s.zone_creation_method] == 'NUMBER_OF_ZONES':
        params[s.number_of_zones] = request_params[s.number_of_beats]

    return params


def create_output_zip_file(beat_name):
    with ZipFile(f'{s.output_path}/{beat_name}.zip', 'w') as zip_obj:
        zip_obj.write(f'{s.output_path}/{beat_name}.cpg', f'{beat_name}.cpg')
        zip_obj.write(f'{s.output_path}/{beat_name}.dbf', f'{beat_name}.dbf')
        zip_obj.write(f'{s.output_path}/{beat_name}.prj', f'{beat_name}.prj')
        zip_obj.write(f'{s.output_path}/{beat_name}.sbn', f'{beat_name}.sbn')
        zip_obj.write(f'{s.output_path}/{beat_name}.sbx', f'{beat_name}.sbx')
        zip_obj.write(f'{s.output_path}/{beat_name}.shp', f'{beat_name}.shp')
        zip_obj.write(f'{s.output_path}/{beat_name}.shp.xml', f'{beat_name}.shp.xml')
        zip_obj.write(f'{s.output_path}/{beat_name}.shx', f'{beat_name}.shx')

    return f'{s.output_path}/{beat_name}.zip', f'{beat_name}.zip'


def upload_file_to_s3(filepath, object_name):
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(s.output_s3_bucket_name).upload_file(filepath, f'{s.s3_beats_dir_name}/{object_name}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
