from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, join_room
from flask_cors import CORS
import redis



app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('locations')


socketio = SocketIO(app,cors_allowed_origins="*")
# CORS(app)

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

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')

# uwsgi --http-socket :5000 --plugin python3 --master --wsgi-file app.py --callable app
