#! /bin/bash -x

COIN=${1:-coiniumserv}

cd ${HOME}/src/coin-buildimage/node
sudo -u ${USER} make ${COIN}-node-kill

