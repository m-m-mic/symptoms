// const { Server } = require("socket.io");

// const io = new Server(8000, {});

// io.on("connection", (socket) => {
//   console.log("connected")
//   socket.on("deathcount", deathcount)
// });

const { createServer } = require("http");
const {Server} = require("socket.io")(8000);
var osc = require('node-osc');

const httpServer = createServer();
const io = new osc.Server(8000, "localhost");

io.sockets.on("connection", function (socket) {
  console.log("connected")
  socket.on("deathcount", deathcount)
});

httpServer.listen(8000, "localhost");

function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(220);
  rect(30,30,40,50)
  text(deathcount, 50, 50)
}