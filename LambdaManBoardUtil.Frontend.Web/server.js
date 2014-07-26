var express = require('express');
var app = express();
var path = require('path');
var http = require('http').Server(app);

app.use(express.static(__dirname)); // Current directory is root
//app.use(express.static(path.join(__dirname, 'public'))); //  "public" off of current is root

http.listen(8080, function () {
    console.log('listening on *:8080');
});

var io = require('socket.io').listen(http);

io.on('connection', function (socket) {
    console.log("connection");
    socket.emit('news', { hello: 'world' });
    socket.on('my other event', function (data) {
        console.log(data);
    });
});

console.log("Express server listening on port 8080");