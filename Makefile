all: build

build: carbon-clickhouse
	docker build -t mosquito/carbon-clickhouse .	

carbon-clickhouse: build-image
	docker run -t --rm -v $(shell pwd):/go/bin carbon-clickhouse-builder:latest \
		/usr/local/go/bin/go get github.com/lomik/carbon-clickhouse

build-image:
	docker build -t carbon-clickhouse-builder:latest -f Dockerfile.build .
