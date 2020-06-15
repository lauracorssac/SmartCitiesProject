#!/bin/bash

# Install required packages
sudo apt-get install -y python3;
sudo apt-get install -y python3-pip;
python3 -m pip install -r requirements.txt

echo -e "Requirements downloaded"
