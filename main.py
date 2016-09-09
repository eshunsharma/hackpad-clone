import socketio
import eventlet
from flask import Flask, render_template
from sockets import Sockets
from mongo import Mongo

MONGO_UP = 0
STORE = {}

sio = socketio.Server()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def textbox(name):
	global MONGO_UP
	db = Sockets(name)
	result = db.create_socket()
	if result == 0:
		MONGO_UP = 0
	else:
		MONGO_UP = 1
	return render_template('textbox.html')

@sio.on('connect')
def connect(sid, environ):
	name = environ['HTTP_REFERER'].split('/')[3]
	sio.enter_room(sid, name)
	if MONGO_UP == 1:
		db = Mongo(0)
		data = db.fetch({"session":name, "data": ""})
	else:
		if name in STORE:
			data = STORE[name]
		else:
			data = {"session":name, "data": ""}
			STORE[name] = data

	sio.emit('data', data, room=name)

@sio.on('data')
def message(sid, data):
	if MONGO_UP == 1:
		db = Mongo(0)
		db.update(data)
	else:
		STORE[data['session']] = data
	sio.emit('data', data , room=data['session'])

@sio.on('disconnect')
def disconnect(sid):
	print('disconnect')

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 6200)), app)