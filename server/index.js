const express = require('express');
var bleno = undefined;
const fs = require('fs');
const jsend = require('./jsend');
const data = JSON.parse(fs.readFileSync('data.json'));
let selectedDevice = data[0];
let blenoInitialized = false;

var app = express();

app.listen(3000, () => { console.log('server running') });

function mockDevice(deviceInfo) {
	if (started)
		bleno.stopAdvertising();

	let advertisementData = Buffer.from(deviceInfo.data, 'hex');
	bleno.startAdvertisingWithEIRData(advertisementData);
}

function mockDeviceByIndex(index) {
	selectedDevice = data[index];
	selectedDeviceId = index;
	mockDevice(selectedDevice);
}

function startAdvertisementCallback(error) {
	if (error)
		console.error(error);
	else
		console.log('advertisment started sucessfully');
}

function startBleno() {
	bleno = require('bleno');
	//var BlenoPrimaryService = bleno.PrimaryService;
	blenoInitialized = true;

	bleno.on('stateChange', function (state) {
		console.log('on -> stateChange: ' + state);
		if (state === 'poweredOn') {
			mockDevice(selectedDevice);
		} else {
			bleno.stopAdvertising();
		}
	});

	bleno.on('advertisingStart', function (error) {
		console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

		if (!error) {
			console.log('advertising!');
		}
	});
}

function getState(){
	let state = {
		platform = bleno ? bleno.platform : 'unkown',
		state = bleno ? bleno.state : 'uninitialized',
		address = bleno ? bleno.address : 'unknown',
		rssi = bleno ? bleno.rssi : 'unkown',
		mtu = bleno ? bleno.mtu : 'unkown'
	};
	return state;
}

	let state = getState();	
	res.json(jsend.returnSuccess(state));
});

app.get('/start', (req, res, next) => {
	startBleno();
	let state = getState();
	res.json(jsend.returnSuccess(state));
});

app.get('/start', (req, res, next) => {
	startBleno();
	res.json("ok");
});
