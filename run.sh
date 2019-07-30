#!/bin/bash
WF="/home/ovalenzuela/Projects/rss2reMarkable/"

cd $WF
git pull
python rssFetcher.py > /dev/null 2>&1