IMAGES := base mxe rpilinux osxcross
DONEFILES := $(addprefix done., ${IMAGES})

#.PHONY: ${IMAGES}

all:	${IMAGES}

%:	done.%
	touch $<

${DONEFILES}:	$(@:done.%=Dockerfile.%) $(FORCE)
	docker build -t beirdo/coin-buildimage:$(@:done.%=%) \
		-f $(@:done.%=Dockerfile.%) ${CACHE} .
	docker push beirdo/coin-buildimage:$(@:done.%=%)
