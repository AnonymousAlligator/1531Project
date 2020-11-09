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
import standup

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

APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='20t3tue17grape1@gmail.com',
    MAIL_PASSWORD='termalmostover2020'
)


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
    data = request.json
    return dumps(auth.auth_login(data['email'], data['password']))

@APP.route('/auth/logout', methods = ['POST'])
def http_auth_logout():
    data = request.json
    return dumps(auth.auth_logout(data['token']))

@APP.route('/auth/register', methods = ['POST'])
def http_auth_register():
    data = request.json
    return dumps(auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last']))

@APP.route('/auth/passwordreset/request', methods=['POST'])
def intermediate_auth_passwordreset_request():
    data = request.json
    return dumps(auth.auth_passwordreset_request(data['email']))

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def intermediate_auth_passwordreset_reset():
    data = request.json
    return dumps(auth.auth_passwordreset_reset(data['reset_code'], data['new_password']))

@APP.route("/channel/invite", methods=['POST'])
def http_channel_invite():
    data = request.json
    return dumps(channel.channel_invite(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route("/channel/details", methods=['GET'])
def http_channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(channel.channel_details(token, int(channel_id)))

@APP.route("/channel/messages", methods=['GET'])
def http_channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    return dumps(channel.channel_messages(token, int(channel_id), int(start)))

@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    data = request.json
    return dumps(channel.channel_leave(data['token'], int(data['channel_id'])))

@APP.route("/channel/join", methods=['POST'])
def http_channel_join():
    data = request.json
    return dumps(channel.channel_join(data['token'], int(data['channel_id'])))

@APP.route("/channel/addowner", methods=['POST'])
def http_channel_jaddowner():
    data = request.json
    return dumps(channel.channel_addowner(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route("/channel/removeowner", methods=['POST'])
def http_channel_removeowner():
    data = request.json
    return dumps(channel.channel_removeowner(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route("/channels/list", methods=['GET'])
def http_channels_list():
    token = request.args.get('token')
    return dumps(channels.channels_list(token))

@APP.route("/channels/listall", methods=['GET'])
def http_channels_listall():
    token = request.args.get('token')
    return dumps(channels.channels_listall(token))

@APP.route("/channels/create", methods=['POST'])
def http_channels_create():
    data = request.json
    return dumps(channels.channels_create(data['token'], data['name'], data['is_public']))

@APP.route("/message/send", methods=['POST'])
def http_message_send():
    data = request.json
    return dumps(message.message_send(data['token'], int(data['channel_id']), data['message']))

@APP.route("/message/sendlater", methods=['POST'])
def http_message_sendlater():
    data = request.json
    return dumps(message.message_sendlater(data['token'], int(data['channel_id']), data['message'], int(data['time_sent'])))

@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    data = request.json
    return dumps(message.message_remove(data['token'], int(data['message_id'])))

@APP.route("/message/edit", methods=['PUT'])
def http_message_edit():
    data = request.json
    return dumps(message.message_edit(data['token'], int(data['message_id']), data['message']))

@APP.route("/message/react", methods=['POST'])
def http_message_react():
    data = request.json
    return dumps(message.message_react(data['token'], int(data['message_id']), int(data['react_id'])))

@APP.route("/message/unreact", methods=['POST'])
def http_message_unreact():
    data = request.json
    return dumps(message.message_unreact(data['token'], int(data['message_id']), int(data['react_id'])))
@APP.route("/message/pin", methods=['POST'])
def http_message_pin():
    data = request.json
    return dumps(message.message_pin(data['token'], int(data['message_id'])))

@APP.route("/message/unpin", methods=['POST'])
def http_message_unpin():
    data = request.json
    return dumps(message.message_unpin(data['token'], int(data['message_id'])))

@APP.route("/user/profile", methods=['GET'])
def http_user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return dumps(user.user_profile(token, int(u_id)))

@APP.route("/user/profile/sethandle", methods = ['PUT'])
def http_user_profile_sethandle():
    data = request.json
    return dumps(user.user_profile_sethandle(data['token'], data['handle_str']))

@APP.route('/user/profile/setemail', methods=['PUT'])
def http_user_profile_setemail():
    data = request.json
    return dumps(user.user_profile_setemail(data['token'], data['email']))

@APP.route('/user/profile/setname', methods=['PUT'])
def http_user_profile_setname():
    data = request.json
    return dumps(user.user_profile_setname(data['token'], data['name_first'], data['name_last']))

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    token = request.args.get('token')
    return dumps(other.users_all(token))

@APP.route("/admin/userpermission/change", methods = ['POST'])
def http_admin_userpermission_change():
    data = request.json
    return dumps(other.admin_userpermission_change(data['token'], int(data['u_id']), int(data['permission_id'])))

@APP.route("/search", methods=['GET'])
def http_search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(other.search(token, query_str))

@APP.route("/standup/start", methods=['POST'])
def http_standup_start():
    data = request.json
    return dumps(standup.standup_start(data['token'], int(data['channel_id']), int(data['length'])))

@APP.route("/standup/active", methods=['GET'])
def http_standup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(standup.standup_active(token, int(channel_id)))

@APP.route("/standup/send", methods=['POST'])
def http_standup_send():
    data = request.json
    return dumps(standup.standup_send(data['token'], int(data['channel_id']), data['message']))

@APP.route("/clear", methods=['DELETE'])
def http_clear():
    return dumps(other.clear())

if __name__ == "__main__":
    APP.run(port=0, debug=True) # Do not edit this port
