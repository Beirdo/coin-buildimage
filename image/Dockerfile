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
	build-essential \
	bzip2 \
	cmake \
	flex \
	g++ \
	gettext \
	git \
	g++-multilib libc6-dev-i386 \
	gperf \
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
	libpng-dev \
	libprotobuf-dev \
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

ENV PATH=${PATH}:/opt/mxe/usr/bin:/opt/cross/bin:/opt/cross/x-tools/arm-unknown-linux-gnueabi/bin

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

# Setup crosstool-ng for Raspberry Pi
WORKDIR /tmp/src/crosstool-pi
ADD crosstool-ng-config-pi .config
RUN ct-ng build

# User creation
WORKDIR /
RUN useradd -m -c "Coin Builder" -d /home/coinbld coinbld
RUN mkdir -p /home/coinbld/src /home/coinbld/artifacts
RUN chown -R coinbld /home/coinbld

# Cleanup
RUN rm -rf /tmp /opt/mxe/pkg /opt/mxe/src
RUN mkdir /tmp
RUN chmod 1777 /tmp
RUN apt-get clean
