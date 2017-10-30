all:

.PHONY: FORCE

COINS := mudcoin peercoin flappycoin buzzcash alexandrite gaincoin saturn2coin
COINS += satori nimbus

${COINS}:: FORCE
	mkdir -p build/$@
	./substitute.py --coin $@

${COINS}:: %: build/%/Dockerfile

${COINS}:: FORCE
	${MAKE} -C build/$@
