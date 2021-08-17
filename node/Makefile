all:

.PHONY: force

COINS := coiniumserv mudcoin peercoin flappycoin buzzcash alexandrite
COINS += satori saturn2coin helium yiimp segacoin gaincoin gsave travelflex
COINS += ppcoin lemmings raincoin rainbowlite wayawolf

MAKEFILES = $(addprefix build/, $(addsuffix /Makefile, ${COINS} base))
DOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile, ${COINS}))
NODEDOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile.node, ${COINS}))
POOLDOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile.pool, ${COINS}))
EXPLORERDOCKERFILES = $(addprefix build/, $(addsuffix /Dockerfile.explorer, ${COINS}))
NODES = $(addsuffix -node, ${COINS})
POOLNODES = $(addsuffix -node-pool, ${COINS})
KILLNODES = $(addsuffix -node-kill, ${COINS})
EXPLORERNODES = $(addsuffix -node-explorer, ${COINS})

${MAKEFILES}:: templates/Makefile.in
${DOCKERFILES}:: templates/Dockerfile.in
${NODEDOCKERFILES} ${EXPLORERDOCKERFILES}:: templates/Dockerfile.node.in
${POOLDOCKERFILES}:: templates/Dockerfile.coiniumserv.in templates/Dockerfile.yiimp.in

${COINS} base:: $(FORCE)
	mkdir -p build/$@ build/cache

NODEJS = node-v8.7.0-linux-x64.tar.xz

build/cache/${NODEJS}:
	wget http://build-artifacts.mycryptocoins.net/${NODEJS} \
		-O build/cache/${NODEJS}

${DOCKERFILES}:: build/cache/${NODEJS}

${DOCKERFILES}:: $(FORCE)
	./substitute.py --coin ${@:build/%/Dockerfile=%}

${POOLDOCKERFILES}:: $(FORCE)
	./substitute.py --coin ${@:build/%/Dockerfile.pool=%} --nodaemon --pool

${NODEDOCKERFILES}:: $(FORCE)
	./substitute.py --coin ${@:build/%/Dockerfile.node=%} --nodaemon

${EXPLORERDOCKERFILES}:: $(FORCE)
	./substitute.py --coin ${@:build/%/Dockerfile.explorer=%} --nodaemon --explorer

${MAKEFILES}:: $(FORCE)
	./substitute.py --coin ${@:build/%/Makefile=%} --makefile

build/base/Dockerfile::	Dockerfile.base $(FORCE)
	cp $< $@

ifneq (${CODEBUILD},1}
${COINS}:: base
endif

${COINS} base:: %: build/%/Dockerfile build/%/Makefile
${COINS} base:: %: $(FORCE)
	${MAKE} -C build/$@ image-done CACHE=${CACHE} FORCE=${FORCE}

${NODES}:: COIN = ${@:%-node=%}
${NODES}:: %-node: % build/%/Dockerfile.node build/%/Makefile
${NODES}:: %-node: $(FORCE)
	mkdir -p build/${COIN}
	${MAKE} -C build/${COIN} node CACHE=${CACHE} FORCE=${FORCE}

${POOLNODES}:: COIN = ${@:%-node-pool=%}
${POOLNODES}:: %-node-pool: % build/%/Dockerfile.pool build/%/Makefile
${POOLNODES}:: %-node-pool: $(FORCE)
	mkdir -p build/${COIN}
	${MAKE} -C build/${COIN} node-pool CACHE=${CACHE} FORCE=${FORCE}


${EXPLORERNODES}:: COIN = ${@:%-node-explorer=%}
${EXPLORERNODES}:: %-node-explorer: % build/%/Dockerfile.explorer build/%/Makefile
${EXPLORERNODES}:: %-node-explorer: $(FORCE)
	mkdir -p build/${COIN}
	${MAKE} -C build/${COIN} node-explorer CACHE=${CACHE} FORCE=${FORCE}


${KILLNODES}:: COIN = ${@:-node-kill=}
${KILLNODES}:: $(FORCE)
	${MAKE} -C build/${COIN} kill-nodes FORCE=${FORCE}

