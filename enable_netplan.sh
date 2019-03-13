#!/bin/bash

 
if [ "$1" = "1" ]; then
	echo "Enabling netplan..." 
	sudo mv /etc/netplan/not_01-netcfg.yaml /etc/netplan/01-netcfg.yaml
	sudo mv /etc/netplan/not_01-network-manager-all.yaml /etc/netplan/01-network-manager-all.yaml
else
	echo "Disabling netplan..."
	sudo mv /etc/netplan/01-netcfg.yaml /etc/netplan/not_01-netcfg.yaml
        sudo mv /etc/netplan/01-network-manager-all.yaml /etc/netplan/not_01-network-manager-all.yaml
fi

