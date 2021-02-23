from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, join_room
from flask_cors import CORS


socketio = SocketIO()
migrate = Migrate()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9OLWxhjlfkl89035jkllkND4o83'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://phpmyadmin:root@127.0.0.1/db_dropit?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # JWT Configurations
    # Setup the flask-jwt-extended extension. See:
    ACCESS_EXPIRES = timedelta(minutes=50)
    REFRESH_EXPIRES = timedelta(days=180)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'
    socketio.init_app(app,cors_allowed_origins="*")
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    return app
