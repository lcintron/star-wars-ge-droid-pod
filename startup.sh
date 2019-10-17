#!/bin/bash

sleep 20

cd ./server

/usr/local/bin/node index.js &

cd ../ui

python main.py



