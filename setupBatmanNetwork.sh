#!/usr/bin/env bash
# Script arguments
 
# ip address
ARG1=${1:-192.168.100.19}
# mtu 
ARG2=${2:-1500}
# frequency
ARG3=${3:-2412}

sudo systemctl stop NetworkManager

#get wifi adapter's logical name (for VM and machine with no wireless card)
#devID=$(iw dev | awk '$1=="Interface"{print $2}')

#get wifi adapter's logical name (for machines with wireless cards)
devID=wlp58s0

#set ip address on VM
sudo ip addr add $ARG1 dev $devID

#set mtu
sudo ip link set $devID mtu $ARG2

sudo iw dev $devID set type ibss

#bring the device online
sudo ip link set $devID up

sudo iw dev $devID ibss join MARBLE $ARG3 HT20 fixed-freq 02:0f:00:73:09:97

#bring up BATMAN-adv
sudo ip link add name bat0 type batadv

#add the interface
sudo ip link set dev $devID master bat0

sudo ip link set up dev bat0

sudo ip addr add $ARG1 dev bat0

#sudo ip addr flush dev $devID







