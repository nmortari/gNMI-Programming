# Created by Nick Mortari
# Technical Marketing Engineer
# Cisco Systems - Cloud Networking Team

# This Python script uses pyGNMI to.
# This script is only a demonstration of how to use gNMI to remotely collect data and configure network devices. It can be used as a starting point for further network development.


#!/usr/bin/evn python

# https://github.com/akarneliuk/pygnmi/tree/master
from pygnmi.client import gNMIclient
import time

# Path to find intermediate CA cert to connect to devices
CertPath = "/home/nick/gnmic/ca-chain.cert.pem"

# List of devices to configure. All information listed here will be iterated through for each switch
# DevicesList = [
    # {
        # "IP":"10.0.1.4",
        # "Port":"50051",
        # "Hostname":"RU31",
        # "Username":"admin",
        # "Password":"Cisco123",
        # "ASN":"65000",
        # "RouterID":"200.0.0.2",
        # "AddressType":"ipv4-ucast",
        # "AddressFamilyNetwork":"2.2.2.0/24",
        # "BGPNeighbor":"200.0.0.1",
        # "NeighborASN":"65001",
        # "NeighborDescription":"RU32 65001",
        # "UpdateValue":"10",
        # "HoldValue":"20",
        # "NeighborAddressType":"ipv4-ucast"
    # },
    # {
        # "IP":"10.0.1.3",
        # "Port":"50051",
        # "Hostname":"leaf2",
        # "Username":"admin",
        # "Password":"Cisco123",
        # "ASN":"65001",
        # "RouterID":"200.0.0.1",
        # "AddressType":"ipv4-ucast",
        # "AddressFamilyNetwork":"1.1.1.0/24",
        # "BGPNeighbor":"200.0.0.2",
        # "NeighborASN":"65000",
        # "NeighborDescription":"RU31 65000",
        # "UpdateValue":"10",
        # "HoldValue":"20",
        # "NeighborAddressType":"ipv4-ucast"
    # }
# ]

if __name__ == '__main__':
    for switch in DevicesList:
        print("Switch " + switch["IP"])
        with gNMIclient(target=(switch["IP"],switch["Port"]),username=switch["Username"],password=switch["Password"],path_cert=CertPath,override=switch["Hostname"]) as gc:
            GetHostname = [
                (
                    "/System/name", #native model
                )
            ]

            gc.get(path=GetHostname)

            print(GetHostname)