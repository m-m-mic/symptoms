let deaths = 0;
let active = false;
let headlinesLoaded = true;
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
  na1: [80, 320],
  na2: [380, 390],
  eu1: [1060, 280],
  sa1: [440, 930],
  sa2: [620, 660],
  af1: [900, 440],
  af2: [1190, 530],
  af3: [1100, 780],
  as1: [1450, 490],
  as2: [1700, 310],
  as3: [1310, 290],
  oc1: [1840, 650],
};

function setup() {
  createCanvas(1920, 1080);
  setupOsc(12000, 3334);
}

let wildfire;
let drought;
let hurricane;
let flooding;
let tsunami;
let earthquake;
let sandstorm;
let annihilation;
let kohoMedium;
let kohoBold;

function preload() {
  wildfire = loadImage("assets/wildfire.png");
  drought = loadImage("assets/drought.png");
  hurricane = loadImage("assets/hurricane.png");
  flooding = loadImage("assets/flooding.png");
  tsunami = loadImage("assets/tsunami.png");
  earthquake = loadImage("assets/earthquake.png");
  sandstorm = loadImage("assets/sandstorm.png");
  annihilation = loadImage("assets/annihilation.png");
  kohoMedium = loadFont("assets/KoHo-Medium.ttf");
  kohoBold = loadFont("assets/KoHo-Bold.ttf");
}

function draw() {
  background(0, 40);
  var deathNumbers = reformatNumber(deaths);
  fill(255);
  textSize(64);
  textFont(kohoBold);
  textAlign(CENTER, CENTER);
  text(deathNumbers + " TOTE", width / 2, 20);

  let regions = Object.keys(regionLocations);

  if (active === false) {
    regions.forEach(function (item, index) {
      fill(66, 135, 245, 255);
      circle(regionLocations[item][0], regionLocations[item][1], 150);
    });
    textSize(48);
    textFont(kohoMedium);
    fill(255);
    text("Berühre einen leuchtenden Punkt um das Spiel zu starten", width / 2, 90);
  } else {
    if (!headlinesLoaded) {
      fill(7, 72, 171);
      rectMode(CENTER);
      noStroke();
      rect(width / 2, height / 2, 1200, 150, 12);
      fill(255);
      textSize(48);
      textFont(kohoMedium);
      text("Schlagzeilen werden generiert, bitte warten...", width / 2, height / 2 - 10);
    }
    regions.forEach(function (item, index) {
      if (regionData[item].is_active) {
        let catastropheType;
        switch (regionData[item].type) {
          case "hurricane":
            catastropheType = hurricane;
            break;
          case "sandstorm":
            catastropheType = sandstorm;
            break;
          case "wildfire":
            catastropheType = wildfire;
            break;
          case "drought":
            catastropheType = drought;
            break;
          case "flooding":
            catastropheType = flooding;
            break;
          case "earthquake":
            catastropheType = earthquake;
            break;
          case "tsunami":
            catastropheType = tsunami;
            break;
          case "annihilation":
            catastropheType = annihilation;
            break;
          default:
            catastropheType = wildfire;
        }
        imageMode(CENTER);
        image(
          catastropheType,
          regionLocations[item][0],
          regionLocations[item][1],
          150 * regionData[item].resolution_percentage,
          150 * regionData[item].resolution_percentage
        );
      }
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
  } else if (address === "/are_headlines_loaded") {
    headlinesLoaded = value[0];
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
