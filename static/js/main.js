var socket = io('http://162.213.199.46:6200');
var txtarea = document.getElementById("text");
var sess = window.location.pathname.replace('/', '');

socket.on('connect', function(){
	console.log('Connection Successful with session: ' + sess);
});

var sendSocket = function() {
	socket.emit('data', {session: sess, data: txtarea.value});
}

txtarea.onkeyup = sendSocket;

txtarea.onblur = sendSocket;

socket.on('data', function(data){
	txtarea.value = data['data'];
});

socket.on('disconnect', function(){
	console.log('Connection Closed')
});