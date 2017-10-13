FROM ubuntu:17.04
MAINTAINER gjhurlbu@gmail.com

# Setup base system
RUN apt-get update && apt-get install -y \
	-o Dpkg::Options::="--force-overwrite" \
	build-essential \
	git \
	make \
	libqt5webkit5-dev \
	libqt5gui5 \
	libqt5core5a \
	libqt5dbus5 \
	qttools5-dev \
	qttools5-dev-tools \
	libprotobuf-dev \
	protobuf-compiler \
	build-essential \
	libboost-dev \
	libboost-all-dev \
	libboost-system-dev \
	libboost-filesystem-dev \
	libboost-program-options-dev \
	libboost-thread-dev libssl-dev \
	libdb++-dev \
	libminiupnpc-dev \
	libevent-dev \
	libcurl4-openssl-dev \
	libpng-dev \
	qrencode \
	libqrencode-dev \
	autoconf \
	automake \
	libtool \
	bash \
	bison \
	bzip2 \
	cmake \
	flex \
	gettext \
	g++ \
	intltool \
	libffi-dev \
	libltdl-dev \
	libssl-dev \
	libxml-parser-perl \
	openssl \
	patch \
	perl \
	python3 \
	pkg-config \
	scons \
	sed \
	unzip \
	zip \
	wget \
	xz-utils \
	autopoint \
	gperf \
	ruby \
	p7zip-full \
	libtool-bin \
	libgdk-pixbuf2.0-dev \
	g++-multilib libc6-dev-i386
	
# Install MXE
WORKDIR /opt
RUN git clone https://github.com/mxe/mxe.git
WORKDIR /opt/mxe
RUN make -j4 MXE_TARGETS='x86_64-w64-mingw32.static i686-w64-mingw32.static' \
	gcc zlib qtbase qtimageformats qttools libpng miniupnpc boost

ENV PATH=${PATH}:/opt/mxe/usr/bin

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

# User creation
WORKDIR /
RUN useradd -m -c "Coin Builder" -d /home/coinbld coinbld

# Cleanup
RUN rm -rf /tmp /opt/mxe/pkg /opt/mxe/src
RUN mkdir /tmp
RUN chmod 1777 /tmp
RUN apt-get clean
