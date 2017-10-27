#! /bin/bash

apt-get update && apt-get install -y \
	software-properties-common
add-apt-repository ppa:bitcoin/bitcoin
apt-get update && apt-get install -y \
	-o Dpkg::Options::="--force-overwrite" \
	autoconf \
	automake \
	autopoint \
	bash \
	bison \
	build-essential \
	bzip2 \
	cmake \
	flex \
	g++ \
	gawk \
	gettext \
	git \
	g++-multilib libc6-dev-i386 \
	gperf \
	help2man \
	intltool \
	libboost-all-dev \
	libboost-dev \
	libboost-filesystem-dev \
	libboost-program-options-dev \
	libboost-system-dev \
	libboost-thread-dev libssl-dev \
	libcurl4-openssl-dev \
	libdb4.8++-dev \
	libevent-dev \
	libffi-dev \
	libgdk-pixbuf2.0-dev \
	libltdl-dev \
	libminiupnpc-dev \
	libncurses5-dev \
	libpng-dev \
	libprotobuf-dev \
	libpython3.6-dev \
	libqrencode-dev \
	libqt5core5a \
	libqt5dbus5 \
	libqt5gui5 \
	libqt5webkit5-dev \
	libssl-dev \
	libtool \
	libtool-bin \
	libxml-parser-perl \
	make \
	openssl \
	p7zip-full \
	patch \
	perl \
	pkg-config \
	protobuf-compiler \
	python3 \
	python3-dev \
	qrencode \
	qt5-default \
	qttools5-dev \
	qttools5-dev-tools \
	rsync \
	ruby \
	scons \
	sed \
	texinfo \
	unzip \
	wget \
	xz-utils \
	zip
