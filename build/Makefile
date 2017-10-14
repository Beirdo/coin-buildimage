all:

COINS := mudcoin peercoin flappycoin

pull-artifacts:	pull-artifacts.in
	sed -e 's/@ID@/'$(shell id -u)'/g' -e 's/@GROUP@/'$(shell id -g)'/' \
		pull-artifacts.in > pull-artifacts

${COINS}:	pull-artifacts
	docker build -f Dockerfile.$@ -t $@:latest ${CACHE} .
	mkdir -p artifacts
	docker run --rm -i -v ${PWD}/artifacts:/artifacts $@:latest \
		bash -s < pull-artifacts
