from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
    send_from_directory
)

from Project import db
main = Blueprint("main", __name__)

@main.route('/<string:username>/<string:room>')
def index(username, room):
    return render_template('index.html', username=username, room=room)

@socketio.on('join_room')
def handle_join_room_event(data):
    # print(data)
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room']);
    return ''

@socketio.on('draw')
def handle_draw_event(data):
    # join_room(data['room'])
    socketio.emit('draw_client', data, room=data['room'])
    # print(data)
    return ''

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1')
