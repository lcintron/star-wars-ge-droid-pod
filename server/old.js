var bleno = require('bleno');
var BlenoPrimaryService = bleno.PrimaryService;

var droidDataPrefix='03044481';
var manufacturerId = '0183';
var chips = {
        R2: '8201',
        BB: '8202',
        Blue: '8A03'
}

console.log('bleno - echo');

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);
  if (state === 'poweredOn'){
    let droidToAdvertise = {name:'BB', id:droidDataPrefix + chips.BB, properties:['notify', 'indicate']};
    let uuid = [manufacturerId,droidToAdvertise.id];
    let advertisementData = Buffer.from('02010609FF8301030444818202060944524F4944','hex');
    bleno.startAdvertisingWithEIRData(advertisementData);

  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

  if (!error) {
        console.log('advertising!');
  }
});