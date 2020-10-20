import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import user
import other
import auth
import message
import channel
import channels

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

@APP.route('/auth/login', methods = ['POST']) 
def http_auth_login():
    data = request.get_json
    return dumps(auth.auth_login(data['email'], data['password']))

@APP.route('/auth/logout', methods = ['POST']) 
def http_auth_logout():
    data = request.get_json
    return dumps(auth.auth_logout(data['token']))

@APP.route('/auth/register', methods = ['POST']) 
def http_auth_register():
    data = request.get_json
    return dumps(auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last']))

@APP.route("/channel/invite", methods=['POST'])
def http_channel_invite():
    data = request.get_json()
    return dumps(channel.channel_invite(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channel/details", methods=['GET'])
def http_channel_details():
    data = request.get_json()
    return dumps(channel.channel_details(data['token'], data['channel_id']))

@APP.route("/channel/messages", methods=['GET'])
def http_channel_messages():
    data = request.get_json()
    return dumps(channel.channel_messages(data['token'], data['channel_id'], data['start']))

@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    data = request.get_json()
    return dumps(channel.channel_leave(data['token'], data['channel_id']))

@APP.route("/channel/join", methods=['POST'])
def http_channel_join():
    data = request.get_json()
    return dumps(channel.channel_join(data['token'], data['channel_id']))

@APP.route("/channel/addowner", methods=['POST'])
def http_channel_jaddowner():
    data = request.get_json()
    return dumps(channel.channel_addowner(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channel/removeowner", methods=['POST'])
def http_channel_removeowner():
    data = request.get_json()
    return dumps(channel.channel_removeowner(data['token'], data['channel_id'], data['u_id']))

@APP.route("/channels/list", methods=['GET'])    
def http_channels_list():
    data = request.get_json()
    return dumps(channels.channels_list(data['token']))

@APP.route("/channels/listall", methods=['GET'])    
def http_channels_listall():
    data = request.get_json()
    return dumps(channels.channels_listall(data['token']))

@APP.route("/channels/create", methods=['GET'])    
def http_channels_create():
    data = request.get_json()
    return dumps(channels.channels_create(data['token'], data['name'], data['is_public']))

@APP.route("/message/send", methods=['POST'])
def http_message_send():
    data = request.get_json()
    return dumps(message.message_send(data['token'], data['channel_id'], data['message']))

@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    data = request.get_json()
    return dumps(message.message_remove(data['token'], data['message_id']))

@APP.route("/message/edit", methods=['PUT'])
def http_message_edit():
    data = request.get_json()
    return dumps(message.message_edit(data['token'], data['message_id'], data['message']))

@APP.route("/user/profile", methods=['GET'])
def http_user_profile():
    data = request.get_json()
    return dumps(user.user_profile(data['token'], data['u_id']))

@APP.route("/user/profile/sethandle", methods = ['PUT']) 
def http_user_profile_sethandle():
    data = request.get_json()
    return dumps(user.user_profile_sethandle(data['token'], data['handle_str']))

@APP.route('/user/profile/setemail', methods=['PUT'])
def http_user_profile_setemail():
    data = request.get_json()
    return dumps(user.user_profile_setemail(data['token'], data['email']))

@APP.route('/user/profile/setname', methods=['PUT'])
def http_user_profile_setname():
    data = request.get_json()
    return dumps(user.user_profile_setname(data['token'], data['name_first'], data['name_last']))

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

@APP.route("/clear", methods=['DELETE'])
def http_clear():
    return dumps(other.clear())

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
