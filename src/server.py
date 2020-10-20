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

@APP.route("channel/details", methods=['GET'])
def http_channel_details():
    data = request.get_json()
    return dumps(channel.channel_details(data['token'], data['channel_id']))

@APP.route("channel/messages", methods=['GET'])
def http_channel_messages():
    data = request.get_json()
    return dumps(channel.channel_messages(data['token'], data['channel_id'], data['start']))

@APP.route("channel/leave", methods=['POST'])
def http_channel_leave():
    data = request.get_json()
    return dumps(channel.channel_leave(data['token'], data['channel_id']))

@APP.route("channel/join", methods=['POST'])
def http_channel_join():
    data = request.get_json()
    return dumps(channel.channel_join(data['token'], data['channel_id']))

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
