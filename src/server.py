import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import other

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

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    data = request.get_json()
    return dumps(other.users_all(data['token']))

@APP.route("/admin/userpermission/change", methods = ['POST']) 
def http_admin_userpermission_change():
    data = request.get_json()
    return dumps(other.admin_userpermission_change(data['token'], data['u_id'], data['permission_id']))

@APP.route("/search", methods=['GET'])
def http_search():
    data = request.get_json()
    return dumps(other.search(data['token'], data['query_str']))

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
