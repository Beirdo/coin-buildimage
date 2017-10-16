all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash
DOCKERFILES = $(addsuffix /Dockerfile, ${COINS})

${DOCKERFILES}:	Dockerfile.in
	mkdir -p ${@:/Dockerfile=}
	./substitute.py --coin ${@:/Dockerfile=} < Dockerfile.in

${COINS}:: %: %/Dockerfile

${COINS}:: FORCE
	docker build -t beirdo/coinnode:$@ ${CACHE} $@
	docker push beirdo/coinnode:$@
