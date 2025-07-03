NODES_DATA := $(shell find . -maxdepth 1 -type d -name '*_data')

genesis_data:
	mkdir genesis_data

shared_data:
	mkdir shared_data

build:
	rm -rf ./atomone
	cp -r ../atomone .
	docker build -t atomone .

config: node_net.dot
	python3 generateNet.py node_net.dot > docker-compose.yaml

run: genesis_data shared_data
	docker compose up -d

node_net.pdf: node_net.dot # requires graphviz installed (brew install graphviz)
	dot -Tpdf -O node_net.dot
	mv node_net.dot.pdf node_net.pdf

stop:
	docker compose down

clean:
	rm -rf $(NODES_DATA)
	@rm -f node_net.pdf 

