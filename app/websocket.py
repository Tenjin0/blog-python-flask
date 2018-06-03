from app import socketio
from flask_login import current_user
from flask import session
from flask_socketio import join_room


@socketio.on('connect', namespace="/notifications")
def connect_notifs():

    if current_user.is_authenticated:
        join_room(session['user_room'])
