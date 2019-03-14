#!/bin/bash

file="/etc/NetworkManager/NetworkManager.conf"

while IFS= read -r line
do
	echo "who"
	echo "$line"
#	if echo "$LINE" | grep -q "managed"; then
#		echo "match"
#	fi
done

