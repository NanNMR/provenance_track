#!/bin/bash
ORIGIN=$(dirname $(readlink -f $0))
cd $ORIGIN
git commit -a
git push
sudo -H pip install git+https://github.com/NanNMR/provenance_track.git 
sudo systemctl restart postgresql@15-main.service
