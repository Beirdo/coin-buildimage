#! /bin/bash -x
if [ "${EUID}" = "0" ] ; then
    umount /mnt
    export USER=ubuntu
fi

cd ${HOME}/src/coin-buildimage
sudo -u ${USER} git pull
for i in `cat poolnodes.txt` ; do
    sudo -u ${USER} /startup-poolnode.sh $i
done
sudo -u ${USER} ./startup-pool.sh

