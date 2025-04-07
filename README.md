# Atomone Dockerized Testnets

The aim of this project download and build the atomone daemon fromgithub and deploy a testnet. The testned is built using isolated docker containers for each node.

The topology of the network is specified in `node_net.dot`. The user can modify the `node_net.dot` to generate different networks. Here, nodes starting with `v` (e.g. `v1`) represent validator nodes, nodes starting with `n` (e.g. `n2`) represents a full node. The node `g0` must be present, and it represent the genesis node - node that will produce the `genesis.json` file - which will become a validator when the blockchain is started.

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

## CLI

These commands are meant to run from a node after getting a shell with `docker exec -it <nodename> /bin/ash`

- Query the list of keys on the node
``` bash
./atomoned keys list  --home /root/atomone_data
# or

./atomoned keys show val_key --home /root/atomone_data
```

- Query balance of address

```bash
./build/atomoned query bank balances atone1lmfyx6r07tllsekq63g24e43c8wssxywncp4k0 --home /root/atomone_data/
```

- Mint Photon
```bash
./build/atomoned tx photon mint 1000atone --chain-id liveness --fees 400uatone --from val_key --home /root/atomone_data/
auth_info:
  fee:
    amount:
    - amount: "400"
      denom: uatone
    gas_limit: "200000"
    granter: ""
    payer: ""
  signer_infos: []
  tip: null
body:
  extension_options: []
  memo: ""
  messages:
  - '@type': /atomone.photon.v1.MsgMintPhoton
    amount:
      amount: "1000"
      denom: atone
    to_address: atone1lmfyx6r07tllsekq63g24e43c8wssxywncp4k0
  non_critical_extension_options: []
  timeout_height: "0"
signatures: []
confirm transaction before signing and broadcasting [y/N]: y
code: 0
codespace: ""
data: ""
events: []
gas_used: "0"
gas_wanted: "0"
height: "0"
info: ""
logs: []
raw_log: '[]'
timestamp: ""
tx: null
txhash: C1A5FB72F16757A00ECFD9810D2023D2CA474631E251DF934F97614DE5D9B935
```
* Show validators 

```bash
./build/atomoned query staking  validators  --home /root/atomone_data/
pagination:
  next_key: null
  total: "0"
validators:
- commission:
    commission_rates:
      max_change_rate: "0.010000000000000000"
      max_rate: "0.200000000000000000"
      rate: "0.100000000000000000"
    update_time: "2025-04-04T10:24:16.744812259Z"
  consensus_pubkey:
    '@type': /cosmos.crypto.ed25519.PubKey
    key: VgBESkzwKKOAUEkzgkjUIU0nOSZUR6qAvItaIA+vpR8=
  delegator_shares: "1000000000.000000000000000000"
  description:
    details: ""
    identity: ""
    moniker: genesis
    security_contact: ""
    website: ""
  jailed: false
  min_self_delegation: "1"
  operator_address: atonevaloper14uxvf2qknlutkw977frdkrl24gzcwry8du3qr5
  status: BOND_STATUS_BONDED
  tokens: "1000000000"
  unbonding_height: "0"
  unbonding_ids: []
  unbonding_on_hold_ref_count: "0"
  unbonding_time: "1970-01-01T00:00:00Z"
- commission:
    commission_rates:
      max_change_rate: "0.010000000000000000"
      max_rate: "0.200000000000000000"
      rate: "0.100000000000000000"
    update_time: "2025-04-04T13:14:37.493012877Z"
  consensus_pubkey:
    '@type': /cosmos.crypto.ed25519.PubKey
    key: a7jn/ELta1+0I8paWYePsaIRY2CO8zBp83z+FnxiHrs=
  delegator_shares: "1100000.000000000000000000"
  description:
    details: ""
    identity: ""
    moniker: validator 1
    security_contact: ""
    website: ""
  jailed: false
  min_self_delegation: "1"
  operator_address: atonevaloper1lmfyx6r07tllsekq63g24e43c8wssxyw392uuh
  status: BOND_STATUS_BONDED
  tokens: "1100000"
  unbonding_height: "0"
  unbonding_ids: []
  unbonding_on_hold_ref_count: "0"
  unbonding_time: "1970-01-01T00:00:00Z"

```
* Delegate tokens for stake 
```bash
./build/atomoned tx staking delegate  atonevaloper1lmfyx6r07tllsekq63g24e43c8wssxyw392uuh 1000000uatone --from val_key --chain-id live
ness --gas auto --fees 400uphoton --home /root/atomone_data/
gas estimate: 133990
auth_info:
  fee:
    amount:
    - amount: "400"
      denom: uphoton
    gas_limit: "133990"
    granter: ""
    payer: ""
  signer_infos: []
  tip: null
body:
  extension_options: []
  memo: ""
  messages:
  - '@type': /cosmos.staking.v1beta1.MsgDelegate
    amount:
      amount: "1000000"
      denom: uatone
    delegator_address: atone1lmfyx6r07tllsekq63g24e43c8wssxywncp4k0
    validator_address: atonevaloper1lmfyx6r07tllsekq63g24e43c8wssxyw392uuh
  non_critical_extension_options: []
  timeout_height: "0"
signatures: []
confirm transaction before signing and broadcasting [y/N]: y
code: 0
codespace: ""
data: ""
events: []
gas_used: "0"
gas_wanted: "0"
height: "0"
info: ""
logs: []
raw_log: '[]'
timestamp: ""
tx: null
txhash: 641C965389FF1EED779CC371F810F405112EA40A7FECC4112CE90CD0F2FBE888
/atomone $ ./build/atomoned query staking  validators  --home /root/atomone_data/
pagination:
  next_key: null
  total: "0"
validators:
- commission:
    commission_rates:
      max_change_rate: "0.010000000000000000"
      max_rate: "0.200000000000000000"
      rate: "0.100000000000000000"
    update_time: "2025-04-04T10:24:16.744812259Z"
  consensus_pubkey:
    '@type': /cosmos.crypto.ed25519.PubKey
    key: VgBESkzwKKOAUEkzgkjUIU0nOSZUR6qAvItaIA+vpR8=
  delegator_shares: "1000000000.000000000000000000"
  description:
    details: ""
    identity: ""
    moniker: genesis
    security_contact: ""
    website: ""
  jailed: false
  min_self_delegation: "1"
  operator_address: atonevaloper14uxvf2qknlutkw977frdkrl24gzcwry8du3qr5
  status: BOND_STATUS_BONDED
  tokens: "1000000000"
  unbonding_height: "0"
  unbonding_ids: []
  unbonding_on_hold_ref_count: "0"
  unbonding_time: "1970-01-01T00:00:00Z"
- commission:
    commission_rates:
      max_change_rate: "0.010000000000000000"
      max_rate: "0.200000000000000000"
      rate: "0.100000000000000000"
    update_time: "2025-04-04T13:14:37.493012877Z"
  consensus_pubkey:
    '@type': /cosmos.crypto.ed25519.PubKey
    key: a7jn/ELta1+0I8paWYePsaIRY2CO8zBp83z+FnxiHrs=
  delegator_shares: "1100000.000000000000000000"
  description:
    details: ""
    identity: ""
    moniker: validator 1
    security_contact: ""
    website: ""
  jailed: false
  min_self_delegation: "1"
  operator_address: atonevaloper1lmfyx6r07tllsekq63g24e43c8wssxyw392uuh
  status: BOND_STATUS_BONDED
  tokens: "1100000"
  unbonding_height: "0"
  unbonding_ids: []
  unbonding_on_hold_ref_count: "0"
  unbonding_time: "1970-01-01T00:00:00Z"
```

* Convert `valoper` address to `acc` address
```bash
./build/atomoned debug addr atonevaloper14uxvf2qknlutkw977frdkrl24gzcwry8du3qr5  --home /root/atomone_data/
Address: [175 12 196 168 22 159 248 187 56 190 242 70 219 15 234 170 5 135 12 135]
Address (hex): AF0CC4A8169FF8BB38BEF246DB0FEAAA05870C87
Bech32 Acc: atone14uxvf2qknlutkw977frdkrl24gzcwry80p6ffv
Bech32 Val: atonevaloper14uxvf2qknlutkw977frdkrl24gzcwry8du3qr5
```
* Query validator outstanding rewards

```bash
./build/atomoned query distribution validator-outstanding-rewards atonevaloper1lmfyx6r07tllsekq63g24e43c8wssxyw392uuh --home /root/ato
mone_data/
rewards:
- amount: "198172404.823076923052711800"
  denom: uatone
- amount: "918.260000000000000000"
  denom: uphoton

```

