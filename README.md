# star-wars-ge-droid-pod
Turn your Raspberry Pi Zero into beacons from *Disney Star Wars: Galaxy's Edge* park and watch your custom built *Droid Depot* droids react (just like they do at the Park!.

## Hardware Requirements
-  Raspberrry Pi Zero W 
-  Waveshare 2.13in e-Paper Display Hat
-  (2) Tactile Push Button

## Hardware Setup

1. Wire or solder the tactile push buttons to pins 15 and 20 (& GND). These will be pulled-up.
2. Install e-Paper display to GPIO header.

## Software Setup
Execute the following in a terminal:

1.  Update OS and install dependencies
~~~
sudo apt update
sudo apt install python3-pip python3-pil python3-numpy RPi.GPIO spidev bluetooth bluez libbluetooth-dev libudev-dev npm -y
~~~

2.  Configure Bluetooth service
~~~
sudo service bluetooth stop
sudo update-rc.d bluetooth remove
sudo systemctl stop bluetooth
sudo systemctl disable bluetooth
~~~

3. Install NodeJS
~~~
sudo npm install -g n
sudo n 9
sudo ln -s /usr/local/n/versions/node/9.11.2/ /usr/bin/node` 
sudo setcap cap_net_raw+eip $(eval readlink -f `which node`)
~~~

4. Download & Install e-Ink Paper Display Drivers
~~~
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install
~~~

## Deploy
1.  Navigate to the cloned repository's server directory and run:
```npm install```
2.  Go back to the root of the repository's folder and run:
``` chmod +x startup.sh``` and simply call the script ```./startup.sh``` to execute. 


## Run on Boot

To execute the application everytime the Pi is turned on, add the following line to your ```/etc/rc.local``` file right before the ```exit 0``` line:
~~~
/home/pi/star-wars-ge-droid-pod/startup.sh &
~~~


## Video

[![Alt text](https://i.ytimg.com/vi/qy_UUQxIx-M/hqdefault.jpg)](https://www.youtube.com/watch?v=qy_UUQxIx-M)
