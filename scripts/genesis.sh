#!/bin/ash

create_validator(){
	sleep 10
	/atomone/build/atomoned  tx photon mint 1000000uatone --home ~/atomone_data/ --from val_key  --fees 10uatone -y
}

MY_VALIDATOR_ADDRESS=$(/atomone/build/atomoned keys show val_key -a --keyring-backend test --home /root/atomone_data)
echo "${MY_VALIDATOR_ADDRESS}"> /root/shared_data/validator_${NODEID}_ADDRESS
echo "export PS1=\"${MY_VALIDATOR_ADDRESS}@validator_${NODEID}:\w \$ \"">> /root/.profile
create_validator &
/atomone/build/atomoned start --home /root/atomone_data

