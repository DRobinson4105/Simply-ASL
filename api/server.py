from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
    
socketio = SocketIO(app,debug=True,cors_allowed_origins='*',async_mode='eventlet')

@app.route("/")
def alive():
    return '<h1>I\'m Alive!<h1/>'

@socketio.on('connect')
def handle_connect():
    print("User Connected")
    emit('connected', {'message': 'You are connected :3!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('User disconnected')

@socketio.on('message')
def handle_message(msg):
    print(f"Received msg: {msg}")
    send(f"Echoechoechoechoechoecho: {msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3001)
    
# flask --app server run 