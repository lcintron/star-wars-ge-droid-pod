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

var app = require("node-server-screenshot");
app.fromHTML("<html><body>Hello world!</body></html>", "test.png",{show:false}, function(){
    //an image of the HTML has been saved at ./test.png
        console.log('screenshot created');
});

/*const puppeteer = require('puppeteer-core');

(async () => {
const browser = await puppeteer.launch({
        args: ['--disable-dev-shm-usage'],
        executablePath:'chromium-browser',
        ignoreHTTPSErrors:true,
        headless:true
});

const htmlString = `<html>
<head>
    <title></title>
</head>
<body>
    <div class="container" style="height:200px;width: 200px;border: 1px solid red">
        <header style="height:50px">
            Header
        </header>
        <footer style="height:100px">
            footer
        </footer>
    </div>
</body>
</html>`;


const page = await browser.newPage();

await page.setViewport({
  width: 250,
  height: 122,
  deviceScaleFactor: 1,
  isMobile: true,
  isLandscape:true
});


console.log('navigating!');
await page.setContent(htmlString)


console.log('generating screenshot!');
await page.screenshot({path: 'screenshot.png'});

await browser.close();
console.log('screenshot saved!');
})();
*/
