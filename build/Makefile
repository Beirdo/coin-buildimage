calc=$(shell echo $$\(\($(1)\)\))
TOTALCORES := $(shell nproc)
CORES := $(call calc,"${TOTALCORES} * 3 / 4")
ifeq (${CODEBUILD},1)
CORES := 1
endif
export CORES

all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin netcoin alexandrite gaincoin saturn2coin
COINS += satori nimbus she421 helium gridcoin segacoin gsave travelflex
COINS += lemmings om raincoin litecoinultra rainbowlite wayawolf

DOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile, ${COINS}))

${DOCKERFILES}:: FORCE
	@echo Using -j${CORES}
	mkdir -p ${@:/Dockerfile=}
	./substitute.py --coin ${@:build/%/Dockerfile=%}

${COINS}:: %: build/%/Dockerfile

${COINS}:: FORCE
	${MAKE} -C build/$@ BUILDS=${BUILDS}
