const bleno = require('bleno');
const fs = require('fs');
var BlenoPrimaryService = bleno.PrimaryService;

const data = JSON.parse(fs.readFileSync('data.json'));
let selectedDevice = data[0];
let started = false;
console.log('bleno - echo');

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

function mockDevice(deviceInfo) {
  if(started)
    bleno.stopAdvertising();
  
  let advertisementData = Buffer.from(deviceInfo.data, 'hex');
  bleno.startAdvertisingWithEIRData(advertisementData);
}

function mockDeviceByIndex(index){
  selectedDevice = data[index];
  selectedDeviceId = index;
  mockDevice(selectedDevice);
}

function startAdvertisementCallback(error){
  if(error)
    console.error(error);
  else
    console.log('advertisment started sucessfully');
}