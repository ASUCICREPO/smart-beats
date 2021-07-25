from zipfile import ZipFile

from flask import Flask, request

import uuid
import sys
import subprocess
import settings as s
import boto3

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    request_params = dict(request.form)
    script_params = get_beat_generator_params(request_params)
    print(f'Script params: {script_params}')

    params_as_script_argument = "<param>".join([f"{k}<=>{v}" for k, v in script_params.items()])

    print(params_as_script_argument)

    # Uncomment the lines below after purchasing arcgis-pro license
    # proc = subprocess.run([sys.executable, 'beat_generator.py', params_as_script_argument])
    # print(f'Subprocess return code: {proc.returncode}')

    response_txt = ''
    # if proc.returncode == 0:
    #     print('Script executed successfully')
    #     zip_path, file_name = create_output_zip_file(request_params[s.beat_name])
    #     upload_file_to_s3(zip_path, file_name)
    #     response_txt = file_name

    return response_txt


def get_beat_generator_params(request_params):
    print(f'request params received from web server: {request_params}')
    params = {}

    # Unique Beat name
    beat_name = ''.join([str(uuid.uuid4().hex[:6]), '_beat'])
    params[s.beat_name] = beat_name

    # Polygon-wise crime count shapefile location
    params[s.input_shapefile_path] = 'data/input/census_wise_crime_counts.shp'

    # Build balanced zones params
    params[s.zone_creation_method] = request_params['beat_creation_method']
    params[s.zone_building_criteria_target] = f"count {request_params['cfs_per_beat']} 1"
    params[s.number_of_zones] = request_params['number_of_beats']

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
    print('Uploading file to s3')
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(s.output_s3_bucket_name).upload_file(filepath, f'{s.s3_beats_dir_name}/{object_name}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
