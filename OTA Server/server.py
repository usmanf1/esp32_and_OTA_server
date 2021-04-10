from datetime import datetime
from flask import Flask, request, Response, send_from_directory, make_response, jsonify
from packaging import version
import re
import time
import os
import json
from functools import wraps
import base64


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './bin'
PLATFORMS_JSON = app.config['UPLOAD_FOLDER'] + '/platforms.json'


def log_event(msg):
    st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(st + ' ' + msg)



def load_json():
    platforms = None
    try:
        with open(PLATFORMS_JSON, 'r') as stream:
            platforms = json.load(stream)
    except:
        flash('Error: File not found.')
    if platforms:
        print(platforms)
        return platforms



def check(authorization_header):
    username = "admin"
    password = "password"
    encoded_uname_pass = authorization_header.split()[-1]
    byte_auth = base64.b64encode((username + ":" + password).encode('utf-8'))
    print((byte_auth).decode('utf-8'))
    if encoded_uname_pass == (byte_auth).decode('utf-8'):
        return True

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.headers)
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
        return f(*args, **kwargs)
    return decorated 

def req_validate():
    __dev = request.args.get('dev', default=None)   #device name
    print(request.headers)
    __ver = request.args.get('ver', default=None)
    return __dev, __ver


@app.route('/list', methods=['GET', 'POST'])
@auth_required
def list():
    __error = 400
    platforms = load_json()
    if request.method == 'GET':
        __dev, __ver = req_validate()
        if __dev and __ver:
            log_event("INFO: Dev: " + __dev + " Ver: " + __ver)
            __dev = __dev.lower()
            versions=[]
            if platforms:
                for d in platforms:
                    if __dev == d['hostname']:
                        for ver in d['firmware']:
                            versions.append(ver['version'])
                        
                        return jsonify(versions), 200
                        
                    else:
                        log_event("ERROR: Unknown Device.")
                        return 'Error: Unknown Device.', 400
            else:
                log_event("ERROR: Create platforms before updating.")
                return 'Error: Create platforms before updating.', 500
        log_event("ERROR: Invalid parameters.")
        return 'Error: Invalid parameters.', 400


@app.route('/latest', methods=['GET', 'POST'])
@auth_required
def latest():
    __error = 400
    platforms = load_json()
    if request.method == 'GET':
        __dev, __ver = req_validate()
        if __dev and __ver:
            log_event("INFO: Dev: " + __dev + " Ver: " + __ver)
            __dev = __dev.lower()
            versions=[]
            if platforms:
                for d in platforms:
                    if __dev == d['hostname']:
                        for ver in d['firmware']:
                            versions.append(ver['version'])
                        
                        latest_version = max(versions)
                        for ver in d['firmware']:
                            if version.parse(latest_version) == version.parse(ver['version']):
                                f = ver['path']
                                response = make_response(send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=f,
                                                        as_attachment=True, mimetype='application/octet-stream',
                                                        attachment_filename=f))
                                response.headers['Content-Length'] = os.path.getsize(app.config['UPLOAD_FOLDER']+'/'+f)
                                print(response.headers)
                                return response
                        else:
                            log_event("INFO: No update needed.")
                            return 'No update needed.', 304
                        return jsonify(versions), 200
                        
                    else:
                        log_event("ERROR: Unknown Device.")
                        return 'Error: Unknown Device.', 400
            else:
                log_event("ERROR: Create platforms before updating.")
                return 'Error: Create platforms before updating.', 500
        log_event("ERROR: Invalid parameters.")
        return 'Error: Invalid parameters.', 400
    
@app.route('/update', methods=['GET', 'POST'])
def update():
    __error = 400
    platforms = load_json()
    __dev, __ver = req_validate()
    __update = request.args.get('update', default=None)
    if __dev and __ver and __update:
        log_event("INFO: Dev: " + __dev + " Ver: " + __ver + " Update: "+ __update)
        __dev = __dev.lower()
        if platforms:
            for d in platforms:
                if __dev == d['hostname']:
                    
                    for ver in d['firmware']:
                        if version.parse(__update) == version.parse(ver['version']):
                            f = ver['path']
                            response = make_response(send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=f,
                                                    as_attachment=True, mimetype='application/octet-stream',
                                                    attachment_filename=f))
                            response.headers['Content-Length'] = os.path.getsize(app.config['UPLOAD_FOLDER']+'/'+f)

                            return response
                    else:
                        log_event("INFO: Unknown Version.")
                        return 'Unknown Version.', 400
                    
                else:
                    log_event("ERROR: Unknown platform.")
                    return 'Error: Unknown platform.', 400
        else:
            log_event("ERROR: Create platforms before updating.")
            return 'Error: Create platforms before updating.', 500
    log_event("ERROR: Invalid parameters.")
    return 'Error: Invalid parameters.', 400







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int('8090'), debug=True)
