all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash alexandrite saturn2coin
COINS += satori

DOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile, ${COINS}))
NODEDOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile.node, ${COINS}))
NODES = $(addsuffix -node, ${COINS})
KILLNODES = $(addsuffix -node-kill, ${COINS})

${DOCKERFILES}:: Dockerfile.in
${NODEDOCKERFILES}:: Dockerfile.node.in

${COINS}:: FORCE
	mkdir -p build/$@

${DOCKERFILES} ${NODEDOCKERFILES}::
	[ -f node-v8.7.0-linux-x64.tar.xz ] || \
		wget https://nodejs.org/dist/v8.7.0/node-v8.7.0-linux-x64.tar.xz

${DOCKERFILES}::
	./substitute.py --coin ${@:build/%/Dockerfile=%} < Dockerfile.in

${NODEDOCKERFILES}::
	./substitute.py --coin ${@:build/%/Dockerfile.node=%} \
		--nodaemon < Dockerfile.in

${COINS}:: %: build/%/Dockerfile

${COINS}:: FORCE
	docker build --build-arg CACHE_DATE="$(shell date)" \
		-t beirdo/coinnode:$@ ${CACHE} build/$@
	docker push beirdo/coinnode:$@

${NODES}:: COIN = ${@:-node=}
${NODES}:: FORCE
	mkdir -p build/${COIN}

${NODES}:: %-node: build/%/Dockerfile.node

${NODES}:: FORCE
	docker build -t node:${COIN}  ${CACHE} \
		-f build/${COIN}/Dockerfile.node build/${COIN}
	docker run -d -i -t $(shell cat build/${COIN}/ports.txt) \
		--ulimit core=999999999 --name node_${COIN} \
		node:${COIN} /bin/bash


${KILLNODES}:: COIN = ${@:-node-kill=}
${KILLNODES}:: FORCE
	-docker kill node_${COIN}
	-docker rm node_${COIN}
