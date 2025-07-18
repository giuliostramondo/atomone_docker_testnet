#!/bin/ash

mkdir /root/atomone_data
/atomone/build/atomoned init node_${NODEID} --default-denom uatone --chain-id liveness --home /root/atomone_data
/atomone/build/atomoned config chain-id liveness --home /root/atomone_data
MY_NODE_ID=$(/atomone/build/atomoned tendermint show-node-id --home /root/atomone_data)
/atomone/build/atomoned config keyring-backend test --home /root/atomone_data
/atomone/build/atomoned keys add val_key --home /root/atomone_data
echo "${MY_NODE_ID}@${ADDRESS}:26656"> /root/shared_data/node${NODEID}_ID
sed -i.bak 's#^minimum-gas-prices = .*#minimum-gas-prices = "0.001uatone,0.001uphoton"#g' /root/atomone_data/config/app.toml
cp /root/shared_data/genesis.json /root/atomone_data/config/genesis.json 
PERSISTENT_PEERS=""; for p in ${PEERS};do PERSISTENT_PEERS="`cat /root/shared_data/${p}_ID`,$PERSISTENT_PEERS" ;done
sed -i.bak "s#^persistent_peers = .*#persistent_peers = \"${PERSISTENT_PEERS}\"#g" /root/atomone_data/config/config.toml
WALLET=$(/atomone/build/atomoned keys show val_key -a --keyring-backend test --home /root/atomone_data)
echo "export PS1=\"${WALLET}@node_${NODEID}:\w \$ \"">> /root/.profile
/atomone/build/atomoned start --home /root/atomone_data

