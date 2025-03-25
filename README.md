# Atomone Dockerized Testnets

The aim of this project download and build the atomone daemon fromgithub and deploy a testnet. The testned is built using isolated docker containers for each node.

The topology of the network is specified in `node_net.dot`. Here, nodes starting with `v` (e.g. `v1`) represent validator nodes, nodes starting with `n` (e.g. `n2`) represents a full node. The node `g0` must be present, and it represent the genesis node - node that will produce the `genesis.json` file - which will become a validator when the blockchain is started.

For each pair of linked nodes a separate docker network is created, this implies that if nodes are not linked (using `--`) in `node_net.dot` they will not be able to communicate directly.

Linked nodes are configured to be `persistent_peers` of eachothers.

## Display the Node Net

If graphviz is installed in the system (e.g. `brew install graphviz` on osx), executing `make node_net.pdf` will generate an image representing the network topology.

## Configure docker compose from node_net.dot

The make target 
```
make config
```
will override the docker-compose.yaml file, and configure it according to the topology described in `node_net.dot`

## Usage

### Testnet Generation

The test net is generated using 
```bash
make run
```

This will:
1. let the validators create their wallet keys
2. the genesis node - that will also be a validator - collects the genesis wallets info - data across container is transfered through the `shared_data` folder. It will create the genesis.json file of the network and place it as well in the `shared_data` folder.
3. After, the first two steps, the validators (among which the genesis node), and the full nodes will start the test net.

### Inspect and connect to single nodes

It is possible to check the output of a specific node using:

```bash
docker compose logs <nodename>
```

where `<nodename>` is the name of the container declared in the docker compose file (e.g. validator1).

It is also possible to log in a running node with:

```bash
docker exec -it <nodename> /bin/ash
```

The testnet can be stopped using the `make stop` target. Finally, all the testnet generated files can be removed with `make clean`.
