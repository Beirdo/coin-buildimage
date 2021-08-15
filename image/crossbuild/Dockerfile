FROM localhost:5000/coin-buildimage:base
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
	bzip2 \
	cmake \
        curl \
        file \
	flex \
	g++ \
	gawk \
	gettext \
        git \
	gperf \
	help2man \
	intltool \
	libgcc1 \
	libc-dev:amd64 \
	libc6-dev \
	libc6-dev:arm64 \
	libc6-dev:armhf \
	libc++-dev \
	libc++-dev:arm64 \
	libc++-dev:armhf \
	libxml-parser-perl \
	linux-libc-dev \
	linux-libc-dev:arm64 \
	linux-libc-dev:armhf \
	make \
	mingw-w64-x86-64-dev \
	p7zip-full \
	patch \
	perl \
        pkg-config \
	protobuf-compiler \
	psmisc \
        python \
	python3 \
	qtchooser \
        qttools5-dev-tools \
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
RUN ln -s /usr/osxcross/bin/xcrun /usr/bin
ADD gcc-darwin /usr/osxcross/bin/x86_64-apple-darwin15-gcc
ADD g++-darwin /usr/osxcross/bin/x86_64-apple-darwin15-g++
ADD cpp-darwin /usr/osxcross/bin/x86_64-apple-darwin15-cpp

RUN cp libpng-1.6.37/config.guess db-4.8.30.NC/dist/config.guess
RUN cp libpng-1.6.37/config.sub db-4.8.30.NC/dist/config.sub
RUN chown -R coinbld db-4.8.30.NC/dist

ADD patches/ /tmp/patches/
RUN for i in /tmp/patches/* ; \
	do echo "Patching ${i#/tmp/patches/}" ; \
	cd ${i#/tmp/patches/} ; \
	cat $i/*.patch | patch -p0; \
	cd .. ; \
done
RUN rm -rf /tmp/patches

#ENV PATH=/usr/osxcross/bin:${PATH}
#RUN ln -s /usr/osxcross/SDK/MacOSX10.11.sdk/usr/include /usr/x86_64-apple-darwin15/include
#RUN ln -s /usr/osxcross/SDK/MacOSX10.11.sdk/usr/include /usr/x86_64h-apple-darwin15/include
#RUN ln -s /usr/osxcross/SDK/MacOSX10.11.sdk/usr/include /usr/i386-apple-darwin15/include

CMD ["/bin/bash"]

