all:

.PHONY: FORCE

COINS := coiniumserv mudcoin peercoin flappycoin buzzcash alexandrite
COINS += satori saturn2coin helium yiimp segacoin gaincoin gsave travelflex
COINS += ppcoin lemmings raincoin rainbowlite

DOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile, ${COINS}))
NODEDOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile.node, ${COINS}))
POOLDOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile.pool, ${COINS}))
EXPLORERDOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile.explorer, ${COINS}))
NODES = $(addsuffix -node, ${COINS})
POOLNODES = $(addsuffix -node-pool, ${COINS})
KILLNODES = $(addsuffix -node-kill, ${COINS})
EXPLORERNODES = $(addsuffix -node-explorer, ${COINS})

${DOCKERFILES}:: Dockerfile.in
${NODEDOCKERFILES} ${EXPLORERDOCKERFILES}:: Dockerfile.node.in
${POOLDOCKERFILES}:: Dockerfile.coiniumserv.in Dockerfile.yiimp.in

${COINS}:: FORCE
	mkdir -p build/$@ build/cache

NODEJS = node-v8.7.0-linux-x64.tar.xz

build/cache/${NODEJS}:
	wget http://build-artifacts.mycryptocoins.net/${NODEJS} \
		-O build/cache/${NODEJS}

${DOCKERFILES}:: build/cache/${NODEJS}

${DOCKERFILES}::
	./substitute.py --coin ${@:build/%/Dockerfile=%}

${POOLDOCKERFILES}::
	./substitute.py --coin ${@:build/%/Dockerfile.pool=%} --nodaemon --pool

${NODEDOCKERFILES}::
	./substitute.py --coin ${@:build/%/Dockerfile.node=%} --nodaemon

${EXPLORERDOCKERFILES}::
	./substitute.py --coin ${@:build/%/Dockerfile.explorer=%} --nodaemon --explorer

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

${POOLNODES}:: COIN = ${@:-node-pool=}
${POOLNODES}:: FORCE
	mkdir -p build/${COIN}

${POOLNODES}:: %-node-pool: build/%/Dockerfile.pool

${POOLNODES}:: FORCE
	docker build -t pool:${COIN}  ${CACHE} \
		-f build/${COIN}/Dockerfile.pool build/${COIN}
	docker run -d -i -t $(shell cat build/${COIN}/ports.txt) \
		--ulimit core=999999999 --name pool_${COIN} \
		pool:${COIN} /bin/bash

${EXPLORERNODES}:: COIN = ${@:-node-explorer=}
${EXPLORERNODES}:: FORCE
	mkdir -p build/${COIN}

${EXPLORERNODES}:: %-node-explorer: build/%/Dockerfile.explorer

${EXPLORERNODES}:: FORCE
	docker build -t explorer:${COIN}  ${CACHE} \
		-f build/${COIN}/Dockerfile.explorer build/${COIN}
	docker run -d -i -t $(shell cat build/${COIN}/ports.txt) \
		--ulimit core=999999999 --name explorer_${COIN} \
		explorer:${COIN} /bin/bash


${KILLNODES}:: COIN = ${@:-node-kill=}
${KILLNODES}:: FORCE
	-docker kill node_${COIN} pool_${COIN} explorer_${COIN}
	-docker rm node_${COIN} pool_${COIN} explorer_${COIN}

