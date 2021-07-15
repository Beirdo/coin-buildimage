calc=$(shell echo $$\(\($(1)\)\))

IMAGES := base mxe rpilinux osxcross arm64linux
DONEFILES := $(addprefix done., ${IMAGES})
#CORES := $(call calc,$(shell nproc) \* 3 / 2)
CORES := $(call calc,$(shell nproc) / 2)
export CORES

#.PHONY: ${IMAGES}

all:	${IMAGES}

%:	done.%
	touch $<

${DONEFILES}:	$(@:done.%=Dockerfile.%) $(FORCE)
	@echo Using -j${CORES}
	docker build -t localhost:5000/coin-buildimage:$(@:done.%=%) \
		-f $(@:done.%=Dockerfile.%) ${CACHE} .
	docker push localhost:5000/coin-buildimage:$(@:done.%=%)
