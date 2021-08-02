#!/bin/bash

key="$1"
url="$2"
message="$3"
urlZabbix="$4"
keyZabbix="$5"

/usr/bin/python3 /etc/zabbix/scripts/zendesk.py "$url" "$key" "$message" "$urlZabbix" "$keyZabbix"
