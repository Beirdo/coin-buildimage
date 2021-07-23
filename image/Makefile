IMAGES := crossbuild x86_64-linux aarch64-linux armhf-linux x86_64-windows
IMAGES := ${IMAGES} 1686-windows

.PHONY:	force

all:	${IMAGES}

${IMAGES}:	force
	${MAKE} -C $@ all
