#! /bin/bash

COIN=${1:-mudcoin}

./shutdown.sh ${COIN}
docker rmi beirdo/coinnode:${COIN}
cd /home/ubuntu/src/coin-buildimage/node
sudo -u ubuntu git pull
sudo -u ubuntu make ${COIN}-node

