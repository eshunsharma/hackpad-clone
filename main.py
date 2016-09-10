import socketio
import eventlet
from eventlet import wsgi
from flask import Flask, render_template
from sockets import Sockets
from mongo import Mongo

MONGO_UP = 0
STORE = {}

sio = socketio.Server()
app = Flask(__name__)

@app.route('/')
def index():
	'''Function for root page'''
    return render_template('index.html')


@app.route('/<name>')
def textbox(name):
	'''Function to start a session'''

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
	'''When a user connects, check the session name and send data if in db else send empty'''

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
	'''When a user send some data, store it in db and pass the data to other people in same group'''

	sio.emit('data', data , room=data['session'], skip_sid=sid)
	if MONGO_UP == 1:
		db = Mongo(0)
		db.update(data)
	else:
		STORE[data['session']] = data


@sio.on('disconnect')
def disconnect(sid):
	'''Whenever a user is dissconnected, pass'''

	print('disconnected sid: ', sid)


if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    wsgi.server(eventlet.listen(('', 6200)), app)