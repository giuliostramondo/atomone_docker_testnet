# Atomone Dockerized Testnets

## Folder structure

The scripts expect these empty folders to be created:

```
genesis_data
validator1_data
shared_data
```

## Usage

### Testnet Generation

The test net is generated using 
```bash
make run
```

This will:
1. let the validators create their wallet keys
2. the genesis node - that will also be a validator - collects the genesis wallets info - data across container is transfered through the `shared_data` folder. It will create the genesis.json file of the network and place it as well in the `shared_data` folder.
3. After, the first two steps, the validators (among which the genesis node), will start the test net.

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
