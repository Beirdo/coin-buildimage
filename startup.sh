#! /bin/bash

docker rmi beirdo/coinnode:mudcoin
cd /home/ubuntu/src/coin-buildimage/node
sudo -u ubuntu git pull
sudo -u ubuntu make mudcoin-node

