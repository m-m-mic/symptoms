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
  na1: [120, 490],
  na2: [410, 550],
  eu1: [1040, 460],
  sa1: [440, 1040],
  sa2: [630, 810],
  af1: [890, 620],
  af2: [1170, 690],
  af3: [1080, 920],
  as1: [1420, 650],
  as2: [1650, 480],
  as3: [1280, 470],
  oc1: [1800, 780],
};

function setup() {
  createCanvas(1920, 1080);
  setupOsc(12000, 3334);
}

let wildfire
let drought
let hurricane
let flooding
let tsunami
let earthquake
let sandstorm
let annihilation

function preload() {
  wildfire = loadImage("assets/wildfire.png")
  drought = loadImage("assets/drought.png")
  hurricane = loadImage("assets/hurricane.png")
  flooding = loadImage("assets/flooding.png")
  tsunami = loadImage("assets/tsunami.png")
  earthquake = loadImage("assets/earthquake.png")
  sandstorm = loadImage("assets/sandstorm.png")
  annihilation = loadImage("assets/annihilation.png")
}

const catastropheFunctions = {
  "hurricane": hurricane,
  "drought": drought,
  "hurricane": hurricane,
  "flooding": flooding,
  "tsunami": tsunami,
  "earthquake": earthquake,
  "sandstorm": sandstorm,
  "annihilation": annihilation

}

function draw() {
  background(0, 40);
  var deathNumbers = reformatNumber(deaths);
  fill(255);
  textSize(64);
  textAlign(CENTER, CENTER);
  text(deathNumbers + " Tote", width / 2, 40);

  let regions = Object.keys(regionLocations);

  if (active === false) {
    regions.forEach(function (item, index) {
      fill(32, 180, 156, 255);
      circle(regionLocations[item][0], regionLocations[item][1], 150);
      fill(255);
      textSize(32);
      text(item, regionLocations[item][0], regionLocations[item][1]);
    });
    textSize(48)
    text("Berühre ein leuchtenden Punkt um das Spiel zu starten", width / 2, 110);
    fill(255, 0, 0);
  } else {
    regions.forEach(function (item, index) {
      if (regionData[item].is_active) {
        let catastropheType;
        switch (regionData[item].type) {
          case "hurricane":
            catastropheType = hurricane
            break
          case "sandstorm":
            catastropheType = sandstorm
            break
          case "wildfire":
            catastropheType = wildfire
            break
          case "drought":
            catastropheType = drought
            break
          case "flooding":
            catastropheType = flooding
            break
          case "earthquake":
            catastropheType = earthquake
            break
          case "tsunami":
            catastropheType = tsunami
            break
          case "annihilation":
            catastropheType = annihilation
            break
          default:
            catastropheType = wildfire
        }
        imageMode(CENTER)
        image(catastropheType, regionLocations[item][0], regionLocations[item][1], 150 * regionData[item].resolution_percentage, 150 * regionData[item].resolution_percentage)
      }
      //fill(0, 0, 255, regionData[item].is_active ? 255 : 0);
      //circle(regionLocations[item][0], regionLocations[item][1], 150 * regionData[item].resolution_percentage);
      //fill(255, 255, 255, regionData[item].is_active ? 255 : 0);
      //textSize(32 * regionData[item].resolution_percentage);
      //text(item, regionLocations[item][0], regionLocations[item][1] - 20);
      //text(regionData[item].type, regionLocations[item][0], regionLocations[item][1] + 20);
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
