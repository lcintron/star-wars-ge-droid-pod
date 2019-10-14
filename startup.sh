#!/bin/bash

sleep 20

cd ./ui

python example.py > ui.log &

cd ../server

node index.js > server.log &


