from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
    send_from_directory
)
from Project import db
main = Blueprint("main", __name__)

@app.route('/<string:username>/<string:room>')
def index(username, room):
    return render_template('index.html', username=username, room=room)

@socketio.on('join_room')
def handle_join_room_event(data):
    print(data)
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room']);
    return ''

@socketio.on('positions')
def handle_draw_event(data):
    # join_room(data['room'])
    socketio.emit('mark_position', data, room=data['room'])
    print(data)
    return ''
