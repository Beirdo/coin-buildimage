#! /bin/bash -x

COIN=${1:-mudcoin}

./shutdown.sh ${COIN}
docker rmi beirdo/coinnode:${COIN}
cd ${HOME}/src/coin-buildimage/node
sudo -u ${USER} git pull
sudo -u ${USER} make ${COIN}-node-explorer

