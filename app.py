from Project import socketio, create_app

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, host='localhost', port=3000)

### gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:3000 --reload --threa 10
0
