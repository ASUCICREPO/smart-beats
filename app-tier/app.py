from zipfile import ZipFile

from flask import Flask, render_template, request

import uuid
import sys
import subprocess
import constants as c

app = Flask(__name__)


def update_request_params(request_params):
    # Unique Beat name
    beat_name = ''.join([str(uuid.uuid4().hex[:6]), '_beat'])
    request_params[c.beat_name] = beat_name

    # Polygon-wise crime count shapefile location
    request_params[c.input_shapefile_path] = 'data/input/census_wise_crime_counts.shp'

    # Build balanced zones params
    request_params[c.zone_creation_method] = 'ATTRIBUTE_TARGET'
    request_params[c.zone_building_criteria_target] = 'count 15000 1'
    request_params[c.spatial_constraints] = 'CONTIGUITY_EDGES_ONLY'


def create_output_zip_file(beat_name):
    with ZipFile(f'{c.output_path}/{beat_name}.zip', 'w') as zip_obj:
        zip_obj.write(f'{c.output_path}/{beat_name}.cpg', f'{beat_name}.cpg')
        zip_obj.write(f'{c.output_path}/{beat_name}.dbf', f'{beat_name}.dbf')
        zip_obj.write(f'{c.output_path}/{beat_name}.prj', f'{beat_name}.prj')
        zip_obj.write(f'{c.output_path}/{beat_name}.sbn', f'{beat_name}.sbn')
        zip_obj.write(f'{c.output_path}/{beat_name}.sbx', f'{beat_name}.sbx')
        zip_obj.write(f'{c.output_path}/{beat_name}.shp', f'{beat_name}.shp')
        zip_obj.write(f'{c.output_path}/{beat_name}.shp.xml', f'{beat_name}.shp.xml')
        zip_obj.write(f'{c.output_path}/{beat_name}.shx', f'{beat_name}.shx')

    return f'{c.output_path}/{beat_name}.zip'


@app.route('/')
def index():
    request_params = dict(request.args)

    update_request_params(request_params)

    params_as_script_argument = "<sep1>".join([f"{k}<sep2>{v}" for k, v in request_params.items()])

    print(params_as_script_argument)

    proc = subprocess.run([sys.executable, 'beat_generator.py', params_as_script_argument])
    if proc.returncode == 0:
        print('Script executed successfully')
        zip_file = create_output_zip_file(request_params[c.beat_name])

    print(f'Subprocess return code: {proc.returncode}')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
