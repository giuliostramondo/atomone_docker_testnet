NODES_DATA := $(shell find . -maxdepth 1 -type d -name '*_data')
run:
	docker compose up -d

stop:
	docker compose down

clean:
	for dir in $(NODES_DATA);do cd $${dir}; rm -rf *; cd ..; done

