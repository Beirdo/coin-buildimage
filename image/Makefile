IMAGES := crossbuild x86_64-linux aarch64-linux

.PHONY:	force

all:	${IMAGES}

${IMAGES}:	force
	${MAKE} -C $@ all
