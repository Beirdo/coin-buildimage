all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash alexandrite gaincoin saturn2coin
COINS += satori nimbus she421 helium gridcoin segacoin gsave

DOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile, ${COINS}))

${DOCKERFILES}:: FORCE
	mkdir -p ${@:/Dockerfile=}
	./substitute.py --coin ${@:build/%/Dockerfile=%}

${COINS}:: %: build/%/Dockerfile

${COINS}:: FORCE
	${MAKE} -C build/$@
