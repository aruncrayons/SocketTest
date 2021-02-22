from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, join_room
import gpxpy
import gpxpy.gpx
from flask_cors import CORS
# from flask_celery import Celery
import redis

# Parsing an existing file:
# -------------------------
gpx_file = open('my_gpx_file.gpx', 'r')

gpx = gpxpy.parse(gpx_file)


app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('locations')
# flask_app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# celery = make_celery(app)


socketio = SocketIO(app,cors_allowed_origins="*")
CORS(app)

@app.route('/<string:username>/<string:room>')
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
