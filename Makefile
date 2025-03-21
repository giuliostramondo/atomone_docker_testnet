NODES_DATA := $(shell find . -maxdepth 1 -type d -name '*_data')

genesis_data:
	mkdir genesis_data

shared_data:
	mkdir shared_data

validator1_data:
	mkdir validator1_data

run: genesis_data shared_data
	docker compose up -d

stop:
	docker compose down

clean:
	for dir in $(NODES_DATA);do cd $${dir}; rm -rf *; cd ..; done

