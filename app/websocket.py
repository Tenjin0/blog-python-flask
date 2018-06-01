from app import socketio
from flask_login import current_user
from flask import session

print("websockets imported")


@socketio.on('connect', namespace='/notifications')
def connect_notifs():
    print('user on connect notifications')
    socketio.emit('response', {'meta': 'WS connected'})

    if current_user.is_authenticated():
        user_room = 'user_{}'.format(session['user_id'])
        socketio.join_room(user_room)
        socketio.emit('response', {'meta': 'WS connected'})
