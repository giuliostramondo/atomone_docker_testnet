#!/bin/ash

mkdir /root/atomone_data
/atomone/build/atomoned init genesis --default-denom uatone --chain-id liveness --home /root/atomone_data
/atomone/build/atomoned config chain-id liveness --home /root/atomone_data
/atomone/build/atomoned config keyring-backend test --home /root/atomone_data
/atomone/build/atomoned keys add val_key --home /root/atomone_data
/atomone/build/atomoned genesis add-genesis-account val_key 1000000000000uatone --home /root/atomone_data --keyring-backend test
for validator in /root/shared_data/*; do
	VAL_ADDR=`cat $validator`
	echo "Iterating through validator addresseds :${VAL_ADDR}"
	/atomone/build/atomoned genesis add-genesis-account $VAL_ADDR 1000000000000uatone --home /root/atomone_data 
	/atomone/build/atomoned genesis gentx $VAL_ADDR 1000000000uatone --home /root/atomone_data --chain-id liveness
done
/atomone/build/atomoned genesis gentx val_key 1000000000uatone --home /root/atomone_data --chain-id liveness
/atomone/build/atomoned genesis collect-gentxs --home /root/atomone_data
sed -i.bak 's#^minimum-gas-prices = .*#minimum-gas-prices = "0.001uatone,0.001uphoton"#g' /root/atomone_data/config/app.toml
cp /root/atomone_data/config/genesis.json /root/shared_data/genesis.json
GENESIS_ID=$(/atomone/build/atomoned tendermint show-node-id --home /root/atomone_data)
echo "${GENESIS_ID}@${ADDRESS}:26656"> /root/shared_data/genesis${NODEID}_ID

