let deaths = 0;
let active = false;
let regionData = {
            na1: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            na2: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            eu1: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            sa1: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            sa2: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            af1: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            af2: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            af3: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            as1: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            as2: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            as3: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
            oc1: {
                is_active: false,
                type: "",
                resolution_percentage: 0,
            },
        };
const regionLocations = {
	na1: [100, 500],
	na2: [100, 1000],
	eu1: [100, 1500],
	sa1: [500, 500],
	sa2: [500, 1000],
	af1: [500, 1500],
	af2: [1000, 500],
	af3: [1000, 1000],
	as1: [1000, 1500],
	as2: [1800, 500],
	as3: [1800, 1000],
	oc1: [1800, 1500]
}

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
  	text(deathNumbers, width/2, 40);

	  if (active === false) {
		  text('Berühre ein Ding um das Spiel zu starten', width/2, height/2);
		  fill(255, 0, 0);
	  } else {
		  let regions = Object.keys(regionLocations);
		  console.log(regions);

		  console.log("regions running: ")
		  if(regionData){
			  regions.forEach(function (item, index) {
				  console.log(item);
				  if (regionData[item].is_active) {
					  fill(0, 0, 255);
					  circle(regionLocations[item][0], regionLocations[item][1], 200);
				  }
			  })
		  }
	  }
}

function reformatNumber(number){
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function receiveOsc(address, value) {
	// console.log("received OSC: " + address);
	if(address === "/death_count"){
		deaths = value;
	} else if (address === "/is_game_running") {
		active = value;
	} else if (address === "/region_data") {
		regionData = JSON.parse(value);
	}
}

function sendOsc(address, value) {
	socket.emit('message', [address].concat(value));
  console.log(value)
}

function setupOsc(oscPortIn, oscPortOut) {
	var socket = io.connect('http://127.0.0.1:8081', { port: 8081, rememberTransport: false });
	socket.on('connect', function() {
		socket.emit('config', {
			server: { port: oscPortIn,  host: '127.0.0.1'},
			client: { port: oscPortOut, host: '127.0.0.1'}
		});
	});
	socket.on('message', function(msg) {
		if (msg[0] == '#bundle') {
			for (var i=2; i<msg.length; i++) {
				receiveOsc(msg[i][0], msg[i].splice(1));
			}
		} else {
			receiveOsc(msg[0], msg.splice(1));
		}
	});
}
