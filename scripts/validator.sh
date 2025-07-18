#!/bin/ash

create_validator(){
sleep 10
/atomone/build/atomoned  tx photon mint 1000000uatone --home ~/atomone_data/ --from val_key  --fees 10uatone -y
sleep 10
atomoned tx staking create-validator --amount "100uatone" --from val_key   --moniker="validator1" --commission-rate="0.10" --commission-max-rate="0.20" --commission-max-change-rate="0.01" --min-self-delegation="1" --fees=2000uphoton --pubkey $(atomoned tendermint show-validator --home ~/atomone_data) --chain-id liveness --home ~/atomone_data -y

sleep 10
atomoned tx staking delegate $(atomoned keys show val_key --bech val -a  --home ~/atomone_data)  1000000uatone --from val_key --fees 2000uphoton --home ~/atomone_data -y

}

mkdir /root/atomone_data
/atomone/build/atomoned init validator_${NODEID} --default-denom uatone --chain-id liveness --home /root/atomone_data
/atomone/build/atomoned config chain-id liveness --home /root/atomone_data
MY_VALIDATOR_ID=$(/atomone/build/atomoned tendermint show-node-id --home /root/atomone_data)
echo "${MY_VALIDATOR_ID}@${ADDRESS}:26656"> /root/shared_data/validator${NODEID}_ID
sed -i.bak 's#^minimum-gas-prices = .*#minimum-gas-prices = "0.001uatone,0.001uphoton"#g' /root/atomone_data/config/app.toml
cp /root/shared_data/genesis.json /root/atomone_data/config/genesis.json 
PERSISTENT_PEERS=""; for p in ${PEERS};do PERSISTENT_PEERS="`cat /root/shared_data/${p}_ID`,$PERSISTENT_PEERS" ;done
sed -i.bak "s#^persistent_peers = .*#persistent_peers = \"${PERSISTENT_PEERS}\"#g" /root/atomone_data/config/config.toml
MY_VALIDATOR_ADDRESS=$(/atomone/build/atomoned keys show val_key -a --keyring-backend test --home /root/atomone_data)
echo "export PS1=\"${MY_VALIDATOR_ADDRESS}@validator_${NODEID}:\w \$ \"">> /root/.profile
create_validator &
/atomone/build/atomoned start --home /root/atomone_data 

