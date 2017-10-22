#! /bin/bash -x

COIN=${1:-mudcoin}

cd /home/ubuntu/src/coin-buildimage/node
sudo -u ubuntu make ${COIN}-node-kill

