const express = require('express');
var bleno = undefined;
const fs = require('fs');
const JSend = require('./jsend');
const data = JSON.parse(fs.readFileSync('data.json'));
let selectedDevice = data[0];
let blenoInitialized = false;
const jsend = new JSend();

var app = express();

app.listen(3000, () => { console.log('server running') });

function AdvertiseWithEIRData(data, callback) {
	if (blenoInitialized)
		bleno.stopAdvertising();
	
	startBleno(function(){
		let dataHex = Buffer.from(data, 'hex');
		bleno.startAdvertisingWithEIRData(dataHex);
		if(callback && typeof callback === "function")
			callback()
	});
}

function startAdvertisementCallback(error) {
	if (error)
		console.error(error);
	else
		console.log('advertisment started sucessfully');
}

function startBleno(callback) {
	bleno = require('bleno');
	var BlenoPrimaryService = bleno.PrimaryService;
	blenoInitialized = true;

	bleno.on('stateChange', function (state) {
		console.log('on -> stateChange: ' + state);
		if (state === 'poweredOn') {
			callback();
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
		platform: bleno ? bleno.platform : 'unkown',
		state : bleno ? bleno.state : 'uninitialized',
		address : bleno ? bleno.address : 'unknown',
		rssi: bleno ? bleno.rssi : 'unkown',
		mtu: bleno ? bleno.mtu : 'unkown'
	};
	return state;
}

app.get('/', (req, res, next)=>{

	let state = getState();	
	res.json(jsend.returnSuccess(state));
});

app.get('/start/EIRAdvertisement/:data', (req, res, next) => {
	if(req.params.data){
		console.log("received data to advertise: "+req.params.data);
		AdvertiseWithEIRData(req.params.data, function(){
			let state = getState();
			res.json(jsend.returnSuccess(state));
		});
	}else{
		res.json(jsend.returnFail("EIR Data (string) to advertise is required."));
	}
	
});

app.get('/error', (req, res, next) => {
	//startBleno();
	res.json("ok");
});
