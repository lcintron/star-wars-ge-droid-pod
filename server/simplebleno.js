function SimpleBleno {

    this.bleno = null;
    this.blenoPrimaryService = null;

    function startAdvertisementWithData(data, callback) {
        let dataHex = Buffer.from(data, 'hex');
        this.bleno.startAdvertisingWithEIRData(dataHex, callback && typeof callback === "function" ? callback : null);
    }
}

SimpleBleno.prototype.start = function (callback) {
    this.bleno = require('bleno');
    this.blenoPrimaryService = bleno.PrimaryService;

    this.bleno.on('stateChange', function (state) {
        console.log('on -> stateChange: ' + state);
        if (state === 'poweredOn') {
            callback();
        } else {
            this.bleno.stopAdvertising();
        }
    });

    this.bleno.on('advertisingStart', function (error) {
        console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

        if (!error) {
            console.log('advertising');
        }
    });

    this.bleno.on('advertisingStop', function (error) {
        console.log('on -> advertisingStop: ' + (error ? 'error ' + error : 'success'));

        if (!error) {
            console.log('stopped advertising');
        }
    });
}

SimpleBleno.prototype.advertiseWithEIRData = function (data, callback) {
    stopAdvertisement(function (error) {
        if (error)
            callback(error);
        else {
            console.log('starting ad after stop');
            this.startAdvertisementWithData(data, callback);
        }
    });

    startBleno(function () {
        this.startAdvertisementWithData(data, callback);
    });
}




SimpleBleno.prototype.getState = function () {
    let state = {
        platform: this.bleno ? bleno.platform : 'unkown',
        state: this.bleno ? bleno.state : 'uninitialized',
        address: this.bleno ? bleno.address : 'unknown',
        rssi: this.bleno ? bleno.rssi : 'unkown',
        mtu: this.bleno ? bleno.mtu : 'unkown'
    };
    return state;
}

SimpleBleno.prototype.stopAvertisement = function (callback) {
    if (this.bleno) {
        this.bleno.stopAdvertising(callback);
    } else {
        callback();
    }
}


module.export = SimpleBleno;