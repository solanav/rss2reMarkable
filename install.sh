#!/bin/bash

# Create a virtual environment with python3
virtualenv -p python3 venb

# Install some dependecies
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended

# Download and build rmapi for uploading to reMarkable
go get -u github.com/juruen/rmapi
go build -a github.com/juruen/rmapi

# Instructions
echo "You can now execute rmapi to configure the unique code by executing `./rmapi`"
echo "Once you have configured rmapi, you can run:"
echo "$ ./fetch"
echo "You can also check feeds.txt to configure your RSS feeds. Have fun!"
