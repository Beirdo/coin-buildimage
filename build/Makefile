all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash alexandrite
DOCKERFILES = $(addsuffix /Dockerfile, ${COINS})

${DOCKERFILES}:: Dockerfile.in

${COINS}:: FORCE
	mkdir -p $@

${DOCKERFILES}::
	./substitute.py --coin ${@:/Dockerfile=} < Dockerfile.in

${COINS}:: %: %/Dockerfile

${COINS}:: FORCE
	docker build --build-arg CACHE_DATE="$(shell date)" -f $@/Dockerfile \
		-t $@:latest ${CACHE} .
	mkdir -p artifacts
	docker run --rm -i -v ${PWD}/artifacts:/artifacts $@:latest \
		bash -s < $@/pull-artifacts
