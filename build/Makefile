all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash alexandrite gaincoin saturn2coin
DOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile, ${COINS}))

${DOCKERFILES}:: Dockerfile.in

${COINS}:: FORCE
	mkdir -p $@

${DOCKERFILES}::
	./substitute.py --coin $(@:build/%/Dockerfile=%) < Dockerfile.in

${COINS}:: %: build/%/Dockerfile

${COINS}:: FORCE
	docker build --build-arg CACHE_DATE="$(shell date)" \
		-f build/$@/Dockerfile -t $@:latest ${CACHE} .
	mkdir -p artifacts
	docker run --rm -i -v ${PWD}/artifacts:/artifacts $@:latest \
		bash -s < build/$@/pull-artifacts
