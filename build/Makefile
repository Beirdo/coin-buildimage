all:

.PHONY: FORCE

pull-artifacts:	FORCE
	sed -e 's/@ID@/'$(shell id -u)'/g' -e 's/@GROUP@/'$(shell id -g)'/' \
		pull-artifacts.in > pull-artifacts

mudcoin:	pull-artifacts
	docker build -f Dockerfile.$@ -t $@:latest .
	mkdir -p artifacts
	docker run --rm -i -v ${PWD}/artifacts:/artifacts $@:latest \
		bash -s < pull-artifacts
