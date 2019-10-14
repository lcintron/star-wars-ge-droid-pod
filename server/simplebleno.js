

function SimpleBleno() {
    this.bleno = null;
    this.blenoPrimaryService = null;
}

SimpleBleno.prototype.startAdvertisementWithData = function(data, callback) {
	if(this.bleno){
		let dataHex = Buffer.from(data, 'hex');
        	this.bleno.startAdvertisingWithEIRData(dataHex, callback && typeof callback === "function" ? callback : null);
	}
};

SimpleBleno.prototype.start = function (callback) {
    this.bleno = require('bleno');
    this.blenoPrimaryService = this.bleno.PrimaryService;

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
};

SimpleBleno.prototype.advertiseWithEIRData = function (data, callback) {
    	let self = this;
	this.stopAdvertisement(function (error, uninitialized) {
        	if (error)
            		callback(error);
                else if(uninitialized){
			console.log('powering bleno up!');
			self.start(function(){
				self.startAdvertisementWithData(data, callback);
			});
		}
        	else {
            		console.log('starting advertisement after stop');
            		self.startAdvertisementWithData(data, callback);
        	}
    	});
};


SimpleBleno.prototype.getState = function () {
    let state = {
        platform: this.bleno ? this.bleno.platform : 'unkown',
        state: this.bleno ? this.bleno.state : 'uninitialized',
	advertising:this.bleno && this.bleno._bindings?this.bleno._bindings._advertising:false,
        address: this.bleno ? this.bleno.address : 'unknown',
        rssi: this.bleno ? this.bleno.rssi : 'unkown',
        mtu: this.bleno ? this.bleno.mtu : 'unkown'
    };
    return state;
};

SimpleBleno.prototype.stopAdvertisement = function (callback) {
    if (this.bleno) {
        this.bleno.stopAdvertising(callback);
    } else {
        callback(false, true);
    }
};


module.exports = SimpleBleno;
