all:

COINS := mudcoin peercoin flappycoin buzzcash

pull-artifacts:	pull-artifacts.in
	sed -e 's/@ID@/'$(shell id -u)'/g' -e 's/@GROUP@/'$(shell id -g)'/' \
		pull-artifacts.in > pull-artifacts

${COINS}:	pull-artifacts
	docker build --build-arg CACHE_DATE="$(shell date)" -f Dockerfile.$@ \
		-t $@:latest ${CACHE} .
	mkdir -p artifacts
	docker run --rm -i -v ${PWD}/artifacts:/artifacts $@:latest \
		bash -s < pull-artifacts
