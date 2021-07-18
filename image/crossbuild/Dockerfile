FROM localhost:5000/multiarch/crossbuild:latest
MAINTAINER gjhurlbu@gmail.com

# Setup base system
ADD sources.list.stretch /etc/apt/sources.list
RUN rm -f /etc/apt/sources.list.d/emdebian.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys \
	AA8E81B4331F7F50 \
	04EE7237B7D453EC \
	112695A0E562B32A \
	648ACFD622F3D138 \
	EF0F382A1A7B6500
RUN apt-get update || true
RUN apt-get install -y debian-archive-keyring
RUN apt-get install -y -o Dpkg::Options::="--force-overwrite" \
	software-properties-common \
	autoconf \
	automake \
	autopoint \
	bash \
	bison \
	# build-essential \
	bzip2 \
	cmake \
        curl \
        file \
	flex \
	# g++ \
	gawk \
	gettext \
        git \
	# g++-multilib \
	gperf \
	help2man \
	intltool \
	libgcc1 \
        # libtool \
	# libtool-bin \
	libxml-parser-perl \
	# libzip-dev \
	make \
	p7zip-full \
	patch \
	perl \
        pkg-config \
	protobuf-compiler \
	psmisc \
        python \
	python3 \
	# python3-dev \
	rsync \
	ruby \
	scons \
	sed \
	texinfo \
	unzip \
        vim-nox \
	wget \
	xz-utils \
	zip
RUN apt-get autoremove -y && apt-get clean

# User creation
WORKDIR /
RUN useradd -m -c "Coin Builder" -d /home/coinbld coinbld
RUN mkdir -p /home/coinbld/src /home/coinbld/artifacts /opt/sources/archive
RUN chown -R coinbld /home/coinbld /opt/sources

USER coinbld
ADD sources/ /opt/sources/archive/
WORKDIR /opt/sources

RUN for i in $(cat archive/sourcearchives.txt); do tar xvf archive/$i ; done

USER root
RUN cp libpng-1.6.37/config.guess db-4.8.30.NC/dist/config.guess
RUN cp libpng-1.6.37/config.sub db-4.8.30.NC/dist/config.sub
RUN chown -R coinbld db-4.8.30.NC/dist
