#!/bin/ash

mkdir /root/atomone_data
/atomone/build/atomoned config keyring-backend test --home /root/atomone_data
/atomone/build/atomoned keys add val_key --home /root/atomone_data


