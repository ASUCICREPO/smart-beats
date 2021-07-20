from flask import Flask, render_template, request

import uuid
import sys
import subprocess
import constants as c

app = Flask(__name__)


@app.route('/')
def index():
    request_params = dict(request.args)
    beat_name = ''.join([str(uuid.uuid4().hex[:6]), '_beat'])
    request_params[c.beat_name] = beat_name

    params_as_script_argument = "<sep>".join([f"{k}={v}" for k, v in request_params.items()])

    print(params_as_script_argument)

    proc = subprocess.run([sys.executable, 'beat_generator.py', params_as_script_argument])
    print(f'Subprocess return code: {proc.returncode}')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
