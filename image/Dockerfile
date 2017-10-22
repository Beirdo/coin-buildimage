FROM ubuntu:17.04
MAINTAINER gjhurlbu@gmail.com

# Setup base system
RUN apt-get update && apt-get install -y \
	software-properties-common
RUN add-apt-repository ppa:bitcoin/bitcoin
RUN apt-get update && apt-get install -y \
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
	
# Install MXE
WORKDIR /opt
RUN git clone https://github.com/mxe/mxe.git
WORKDIR /opt/mxe
RUN make -j4 MXE_TARGETS='x86_64-w64-mingw32.static i686-w64-mingw32.static' \
	gcc zlib qtbase qtimageformats qttools libpng miniupnpc boost

ENV PATH=${PATH}:/opt/mxe/usr/bin:/opt/cross/bin:/opt/x-tools/pi-crosstool-ng/arm-unknown-linux-gnueabi/bin

# Build Berkeley DB 4.8 for MXE
WORKDIR /tmp/src
RUN wget http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz
RUN tar -xvf db-4.8.30.NC.tar.gz
WORKDIR /tmp/src/db-4.8.30.NC/build_mxe32
RUN ../dist/configure --host=i686-w64-mingw32.static \
	--prefix=/opt/mxe/usr/i686-w64-mingw32.static --disable-shared \
	--disable-replication --enable-cxx --enable-mingw
RUN make -j4
RUN make install
WORKDIR /tmp/src/db-4.8.30.NC/build_mxe64
RUN ../dist/configure --host=x86_64-w64-mingw32.static \
	--prefix=/opt/mxe/usr/x86_64-w64-mingw32.static --disable-shared \
	--disable-replication --enable-cxx --enable-mingw
RUN make -j4
RUN make install

# Build qrencode for MXE
WORKDIR /tmp/src
RUN wget http://fukuchi.org/works/qrencode/qrencode-3.4.4.tar.gz
RUN tar -xvf qrencode-3.4.4.tar.gz
RUN cp -prv qrencode-3.4.4 qrencode-3.4.4-32
RUN cp -prv qrencode-3.4.4 qrencode-3.4.4-64

WORKDIR /tmp/src/qrencode-3.4.4-32
RUN ./configure --host=i686-w64-mingw32.static \
	--prefix=/opt/mxe/usr/i686-w64-mingw32.static --enable-static \
	--disable-shared --without-tools
RUN make -j4
RUN make install

WORKDIR /tmp/src/qrencode-3.4.4-64
RUN ./configure --host=x86_64-w64-mingw32.static \
	--prefix=/opt/mxe/usr/x86_64-w64-mingw32.static --enable-static \
	--disable-shared --without-tools
RUN make -j4
RUN make install

# Setup crosstool-ng for the Raspberry Pi
WORKDIR /tmp/src
RUN wget http://crosstool-ng.org/download/crosstool-ng/crosstool-ng-1.23.0.tar.xz
RUN tar -xvf crosstool-ng-1.23.0.tar.xz
WORKDIR /tmp/src/crosstool-ng-1.23.0
RUN ./configure --prefix=/opt/cross
RUN make -j4
RUN make install

# User creation
WORKDIR /
RUN useradd -m -c "Coin Builder" -d /home/coinbld coinbld
RUN mkdir -p /home/coinbld/src /home/coinbld/artifacts
RUN chown -R coinbld /home/coinbld

# Setup crosstool-ng for Raspberry Pi
WORKDIR /tmp/src/crosstool-pi
ADD crosstool-ng-config-pi .config
RUN ct-ng oldconfig
RUN ct-ng build

# Setup boost for Raspberry Pi
WORKDIR /tmp/src
RUN wget https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.bz2
RUN tar -xvf boost_1_65_1.tar.bz2
WORKDIR /tmp/src/boost_1_65_1
RUN ./bootstrap.sh
ADD boost-project-config.jam project-config.jam
RUN ./bjam install toolset=gcc-arm --prefix=/opt/x-tools/pi-boost link=static \
	variant=release threading=multi -a -q --reconfigure --without-python

# Build Berkeley DB 4.8 for Raspberry Pi
WORKDIR /tmp/src/db-4.8.30.NC/rpi-build
RUN ../dist/configure --host=arm-unknown-linux-gnueabi \
	--prefix=/opt/x-tools/pi-db --disable-shared \
	--disable-replication --enable-cxx
RUN make -j4
RUN make install

# Build openssl for Raspberry Pi
WORKDIR /tmp/src
RUN wget https://www.openssl.org/source/openssl-1.0.2l.tar.gz
RUN tar -xvf openssl-1.0.2l.tar.gz
WORKDIR /tmp/src/openssl-1.0.2l
ENV CROSS_COMPILE arm-unknown-linux-gnueabi-
RUN ./Configure --cross-compile-prefix=arm-unknown-linux-gnueabi- \
	--prefix=/opt/x-tools/pi-openssl linux-armv4
RUN make -j4
RUN make install

# Build zlib for Raspberry Pi
WORKDIR /tmp/src
RUN wget https://zlib.net/zlib-1.2.11.tar.gz
RUN tar -xvf zlib-1.2.11.tar.gz
WORKDIR /tmp/src/zlib-1.2.11
RUN TARGETMACH=arm-none-linux-gnueabi BUILDMACH=i686-pc-linux-gnu \
	CROSS=arm-none-linux-gnueabi CC=${CROSS_COMPILE}gcc \
	LD=${CROSS_COMPILE}ld AS=${CROSS_COMPILE}-as \
	./configure --prefix=/opt/x-tools/pi-zlib
RUN make -j4
RUN make install

# Cleanup
WORKDIR /
RUN rm -rf /tmp /opt/mxe/pkg /opt/mxe/src
RUN mkdir /tmp ; chmod 1777 /tmp
RUN apt-get clean
