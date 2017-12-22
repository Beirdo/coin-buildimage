all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin netcoin alexandrite gaincoin saturn2coin
COINS += satori nimbus she421 helium gridcoin segacoin gsave travelflex
COINS += lemmings om

DOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile, ${COINS}))

${DOCKERFILES}:: FORCE
	mkdir -p ${@:/Dockerfile=}
	./substitute.py --coin ${@:build/%/Dockerfile=%}

${COINS}:: %: build/%/Dockerfile

${COINS}:: FORCE
	${MAKE} -C build/$@
