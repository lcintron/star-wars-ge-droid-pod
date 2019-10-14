const express = require('express');
var SimpleBleno = require('./simplebleno');
const JSend = require('./jsend');
const jsend = new JSend();
console.log(SimpleBleno);
const simpleBleno = new SimpleBleno();
var app = express();
console.log(simpleBleno);
app.listen(3000, () => { console.log('server running') });

// function AdvertiseWithEIRData(data, callback) {
// 	if (blenoInitialized && bleno){

// 		bleno.stopAdvertising(function(){
// 			console.log('starting ad after stop');
// 			startAdvertisementWithData(data, callback);

// 		});
// 		console.log('stopping adv');
// 	}

// 	startBleno(function(){
// 		startAdvertisementWithData(data,callback);
// 	});
// }

// function startAdvertisementWithData(data,callback){
// 	let dataHex = Buffer.from(data, 'hex');
// 	bleno.startAdvertisingWithEIRData(dataHex,callback && typeof callback === "function"?callback:null);
// }

// function startAdvertisementCallback(error) {
// 	if (error)
// 		console.error(error);
// 	else
// 		console.log('advertisment started sucessfully');
// }

// function startBleno(callback) {
// 	if(!blenoInitialized && bleno == undefined){
// 		bleno = require('bleno');
// 		let BlenoPrimaryService = bleno.PrimaryService;
// 		blenoInitialized = true;

// 		bleno.on('stateChange', function (state) {
// 			console.log('on -> stateChange: ' + state);
// 			if (state === 'poweredOn') {
// 				callback();
// 			} else {
// 				bleno.stopAdvertising();
// 			}
// 		});

// 		bleno.on('advertisingStart', function (error) {
// 			console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

// 			if (!error) {
// 				console.log('advertising!');
// 			}
// 		});

// 		bleno.on('advertisingStop', function(error){
// 			console.log('on -> advertisingStop: ' + (error? 'error ' + error: 'success'));
// 			if(!error){
// 				console.log('not advertising!');
// 			}
// 		});
// 	}

// }

// function getState() {
// 	let state = {
// 		platform: bleno ? bleno.platform : 'unkown',
// 		state: bleno ? bleno.state : 'uninitialized',
// 		address: bleno ? bleno.address : 'unknown',
// 		rssi: bleno ? bleno.rssi : 'unkown',
// 		mtu: bleno ? bleno.mtu : 'unkown'
// 	};
// 	return state;
// }

app.get('/', (req, res, next) => {
	let state = simpleBleno.getState();
	res.json(jsend.returnSuccess(state));
});

app.get('/start/EIRAdvertisement/:data', (req, res, next) => {
	if (req.params.data) {
		console.log("received data to advertise: " + req.params.data);
		simpleBleno.advertiseWithEIRData(req.params.data, function (error) {
			if (error) {
				res.json(jsend.returnError(error));
			} else {
				let state = getState();
				res.json(jsend.returnSuccess(state));
			}
		});
	} else {
		res.json(jsend.returnFail("EIR Data (string) to advertise is required."));
	}

});

app.get('/stop', (req, res, next) => {
	//startBleno();
	res.json("ok");
});
