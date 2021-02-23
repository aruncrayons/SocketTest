from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
    send_from_directory
)
from flask_socketio import join_room, emit
from Project import db, socketio, jwt
# from .blacklist_helpers import is_token_revoked
# from flask_jwt_extended import (
#     create_access_token, create_refresh_token,
#     jwt_required, jwt_refresh_token_required,
#     get_jwt_identity
# )


main = Blueprint("main", __name__)


# Define our callback function to check if a token has been revoked or not
# @jwt.token_in_blacklist_loader
# def check_if_token_revoked(decoded_token):
#     return is_token_revoked(decoded_token)


@main.route('/<string:username>/<string:room>')
def index(username, room):
    return render_template('index.html', username=username, room=room)

# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})

@socketio.on('join_room')
# @jwt_refresh_token_required
def handle_join_room_event(data):
    # print(data)
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room']);
    return ''

@socketio.on('position')
def handle_draw_event(data):
    # join_room(data['room'])
    socketio.emit('mark_position', data, room=data['room'])
    # print(data)
    return ''
