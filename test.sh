#!/bin/bash

# Update all dependencies
echo "updating packages"
sudo apt update
sudo apt upgrade -y

# Clone the telnet-honeypot repository
echo 'downloading the repo'
git clone https://github.com/amedumer/telnet-honeypot.git

# Navigate to the repository directory
cd telnet-honeypot

echo "starting honeypots"
python3 honeypot.py -p 23 &
python3 honeypot.py -p 2323 &