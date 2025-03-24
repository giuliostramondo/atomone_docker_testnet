#!/bin/ash

mkdir /root/atomone_data
/atomone/build/atomoned config keyring-backend test --home /root/atomone_data
/atomone/build/atomoned keys add val_key --home /root/atomone_data
MY_VALIDATOR_ADDRESS=$(/atomone/build/atomoned keys show val_key -a --keyring-backend test --home /root/atomone_data)
echo "${MY_VALIDATOR_ADDRESS}"> /root/shared_data/validator_${NODEID}_ADDRESS


