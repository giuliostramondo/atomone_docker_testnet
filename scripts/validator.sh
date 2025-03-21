#!/bin/ash

mkdir /root/atomone_data
/atomone/build/atomoned init validator_${NODEID} --default-denom uatone --chain-id liveness --home /root/atomone_data
/atomone/build/atomoned config chain-id liveness --home /root/atomone_data
MY_VALIDATOR_ID=$(/atomone/build/atomoned tendermint show-node-id --home /root/atomone_data)
echo $MY_VALIDATOR_ID> /root/shared_data/validator_${NODEID}_ID
sed -i.bak 's#^minimum-gas-prices = .*#minimum-gas-prices = "0.001uatone,0.001uphoton"#g' /root/atomone_data/config/app.toml
cp /root/shared_data/genesis.json /root/atomone_data/config/genesis.json 
GENESIS_ID=`cat /root/shared_data/genesis_0_ID`
sed -i.bak "s#^persistent_peers = .*#persistent_peers = \"${GENESIS_ID}\"#g" /root/atomone_data/config/config.toml
/atomone/build/atomoned start --home /root/atomone_data

