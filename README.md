# star-wars-ge-droid-pod

## Setup
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
sudp install -g n
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

## Run on Boot