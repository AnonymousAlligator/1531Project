import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("channels/list", methods=['GET'])    
def http_channels_list():
    data = request.get_json()
    return dumps(channels.channels_list(data['token']))

@APP.route("channels/listall", methods=['GET'])    
def http_channels_listall():
    data = request.get_json()
    return dumps(channels.channels_listall(data['token']))

@APP.route("channels/create", methods=['GET'])    
def http_channels_create():
    data = request.get_json()
    return dumps(channels.channels_create(data['token'], data['name'], data['is_public']))

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
