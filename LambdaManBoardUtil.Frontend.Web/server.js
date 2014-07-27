var express = require('express');
var app = express();
var path = require('path');
var http = require('http').Server(app);

var zmq = require('zmq'),
    pipeToServer = zmq.socket('push'),
    pipeFromServer = zmq.socket('pull');

app.use(express.static(__dirname)); // Current directory is root
//app.use(express.static(path.join(__dirname, 'public'))); //  "public" off of current is root

http.listen(8080, function () {
    console.log('listening on *:8080');
});

var io = require('socket.io').listen(http);

io.on('connection', function (socket) {
    console.log("New socket.io connection from client");

    //socket.emit('news', { hello: 'world' });
    var initRequest = {
        type: "initRequest"
    };

    pipeToServer.send(JSON.stringify(initRequest));

    socket.on('get_board_state', function (data) {
        //var request = JSON.parse(data);

        console.log("Client wants data from server, " + data.tick);

        pipeToServer.send(JSON.stringify({
            type: "frameRequest",
            params: data.tick
        }));
    });
});

// Forward messages from the backend to the client
pipeFromServer.on('message', function (buf) {
    var message = JSON.parse(buf.toString());
    console.log("message in " + message.type);

    if (message.type == "initResponse") {
        io.sockets.emit('init_response', message.params);
    }

    if (message.type == "frameResponse") {
        io.sockets.emit('frameResponse', message.params);
    }
});

// Completed requests from server
pipeFromServer.connect('tcp://localhost:5557');

// Sends requests to server
pipeToServer.bindSync('tcp://*:5558');

console.log("Connected to server on ports 5557 and 5558");

console.log("Express server listening on port 8080");