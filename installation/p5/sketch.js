let deaths = 0;
let active = false;
let regionData = {
  na1: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  na2: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  eu1: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  sa1: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  sa2: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  af1: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  af2: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  af3: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  as1: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  as2: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  as3: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
  oc1: {
    is_active: true,
    type: "",
    resolution_percentage: 0,
  },
};
const regionLocations = {
  na1: [200, 200],
  na2: [200, 500],
  eu1: [200, 800],
  sa1: [500, 200],
  sa2: [500, 500],
  af1: [500, 800],
  af2: [800, 200],
  af3: [800, 500],
  as1: [800, 800],
  as2: [1100, 200],
  as3: [1100, 500],
  oc1: [1100, 800],
};

function setup() {
  createCanvas(1920, 1080);
  setupOsc(12000, 3334);
}

function draw() {
  background(0, 40);
  var deathNumbers = reformatNumber(deaths);
  fill(255);
  textSize(32);
  textAlign(CENTER, CENTER);
  text(deathNumbers, width / 2, 40);

  let regions = Object.keys(regionLocations);

  if (active === false) {
    regions.forEach(function (item, index) {
      fill(32, 180, 156, 255);
      circle(regionLocations[item][0], regionLocations[item][1], 200);
      fill(255);
      textSize(32);
      text(item, regionLocations[item][0], regionLocations[item][1]);
    });
    text("Berühre ein Ding um das Spiel zu starten", width / 2, height / 2);
    fill(255, 0, 0);
  } else {
    regions.forEach(function (item, index) {
      fill(0, 0, 255, regionData[item].is_active ? 255 : 0);
      circle(regionLocations[item][0], regionLocations[item][1], 200 * regionData[item].resolution_percentage);
      fill(255, 255, 255, regionData[item].is_active ? 255 : 0);
      textSize(32 * regionData[item].resolution_percentage);
      text(item, regionLocations[item][0], regionLocations[item][1] - 20);
      text(regionData[item].type, regionLocations[item][0], regionLocations[item][1] + 20);
    });
  }
}

function reformatNumber(number) {
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function receiveOsc(address, value) {
  if (address === "/death_count") {
    deaths = value;
  } else if (address === "/is_game_running") {
    active = value[0];
  } else if (address === "/region_data") {
    regionData = JSON.parse(value);
  }
}

function sendOsc(address, value) {
  socket.emit("message", [address].concat(value));
  console.log(value);
}

function setupOsc(oscPortIn, oscPortOut) {
  var socket = io.connect("http://127.0.0.1:8081", { port: 8081, rememberTransport: false });
  socket.on("connect", function () {
    socket.emit("config", {
      server: { port: oscPortIn, host: "127.0.0.1" },
      client: { port: oscPortOut, host: "127.0.0.1" },
    });
  });
  socket.on("message", function (msg) {
    if (msg[0] == "#bundle") {
      for (var i = 2; i < msg.length; i++) {
        receiveOsc(msg[i][0], msg[i].splice(1));
      }
    } else {
      receiveOsc(msg[0], msg.splice(1));
    }
  });
}
