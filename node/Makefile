all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash
DOCKERFILES = $(addsuffix /Dockerfile, ${COINS})
NODEDOCKERFILES = $(addsuffix /Dockerfile.node, ${COINS})
NODES = $(addsuffix -node, ${COINS})
KILLNODES = $(addsuffix -node-kill, ${COINS})

${DOCKERFILES}:: Dockerfile.in
${NODEDOCKERFILES}:: Dockerfile.node.in

coindir-%: .PHONY
	mkdir -p ${@:coindir-=}

${DOCKERFILES}::
	./substitute.py --coin ${@:/Dockerfile=} < Dockerfile.in

${NODEDOCKERFILES}::
	./substitute.py --coin ${@:/Dockerfile.node=} < Dockerfile.in

${COINS}:: %: %/Dockerfile | coindir-%

${COINS}:: FORCE
	docker build -t beirdo/coinnode:$@ ${CACHE} $@
	docker push beirdo/coinnode:$@

${NODES}:: COIN = ${@:-node=}
${NODES}:: %-node: %/Dockerfile.node

${NODES}:: FORCE
	docker build -t node:${COIN} ${CACHE} -f ${COIN}/Dockerfile.node ${COIN}
	docker run -d -i -t --ulimit core=99999999 --name node_${COIN} node:${COIN} /bin/bash


${KILLNODES}:: COIN = ${@:-node-kill=}
${KILLNODES}:: FORCE
	-docker kill node_${COIN}
	-docker rm node_${COIN}
