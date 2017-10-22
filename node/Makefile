all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash alexandrite
DOCKERFILES = $(addsuffix /Dockerfile, ${COINS})
NODEDOCKERFILES = $(addsuffix /Dockerfile.node, ${COINS})
NODES = $(addsuffix -node, ${COINS})
KILLNODES = $(addsuffix -node-kill, ${COINS})

${DOCKERFILES}:: Dockerfile.in
${NODEDOCKERFILES}:: Dockerfile.node.in

${COINS}:: FORCE
	mkdir -p $@

${DOCKERFILES}::
	[ -f node-v8.7.0-linux-x64.tar.xz ] || \
		wget https://nodejs.org/dist/v8.7.0/node-v8.7.0-linux-x64.tar.xz
	./substitute.py --coin ${@:/Dockerfile=} < Dockerfile.in

${NODEDOCKERFILES}::
	[ -f node-v8.7.0-linux-x64.tar.xz ] || \
		wget https://nodejs.org/dist/v8.7.0/node-v8.7.0-linux-x64.tar.xz
	./substitute.py --coin ${@:/Dockerfile.node=} --nodaemon < Dockerfile.in

${COINS}:: %: %/Dockerfile

${COINS}:: FORCE
	docker build --build-arg CACHE_DATE="$(shell date)" \
		-t beirdo/coinnode:$@ ${CACHE} $@
	docker push beirdo/coinnode:$@

${NODES}:: COIN = ${@:-node=}
${NODES}:: FORCE
	mkdir -p ${COIN}

${NODES}:: %-node: %/Dockerfile.node

${NODES}:: FORCE
	docker build -t node:${COIN}  ${CACHE} -f ${COIN}/Dockerfile.node \
		${COIN}
	docker run -d -i -t $(shell cat ${COIN}/ports.txt) \
		--ulimit core=999999999 --name node_${COIN} \
		node:${COIN} /bin/bash


${KILLNODES}:: COIN = ${@:-node-kill=}
${KILLNODES}:: FORCE
	-docker kill node_${COIN}
	-docker rm node_${COIN}
