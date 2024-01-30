# Created by Nick Mortari
# Technical Marketing Engineer
# Cisco Systems - Cloud Networking Team

# This Python script uses pyGNMI to remotely configure the BGP service and BGP peering on 2 switches.
# All the XPaths used here are from the Cisco native model.
# This script is only a demonstration of how to use gNMI to remotely configure network devices. It should be used as a starting point for further network development.


#!/usr/bin/evn python

# https://github.com/akarneliuk/pygnmi/tree/master
from pygnmi.client import gNMIclient
import json

# Path to find intermediate CA cert to connect to devices
CertPath = "/home/nick/gnmic/ca-chain.cert.pem"

# List of devices to configure. All information listed here will be iterated through for each switch.
DevicesList = [
    {
        "IP":"10.0.1.4",
        "Port":"50051",
        "Hostname":"RU31",
        "Username":"admin",
        "Password":"Cisco123",
        "ASN":"65000",
        "RouterID":"200.0.0.2",
        "AddressType":"ipv4-ucast",
        "AddressFamilyNetwork":"2.2.2.0/24",
        "BGPNeighbor":"200.0.0.1",
        "NeighborASN":"65001",
        "NeighborDescription":"RU32 65001",
        "UpdateValue":"10",
        "HoldValue":"20",
        "NeighborAddressType":"ipv4-ucast"
    },
    {
        "IP":"10.0.1.3",
        "Port":"50051",
        "Hostname":"leaf2",
        "Username":"admin",
        "Password":"Cisco123",
        "ASN":"65001",
        "RouterID":"200.0.0.1",
        "AddressType":"ipv4-ucast",
        "AddressFamilyNetwork":"1.1.1.0/24",
        "BGPNeighbor":"200.0.0.2",
        "NeighborASN":"65000",
        "NeighborDescription":"RU32 65000",
        "UpdateValue":"10",
        "HoldValue":"20",
        "NeighborAddressType":"ipv4-ucast"
    }
]

# BGP instance name
BGPName="default"
# BGP network address type
AddressType="ipv4-ucast"

if __name__ == '__main__':
    for switch in DevicesList:
        print("Modifying switch " + switch["IP"])
        with gNMIclient(target=(switch["IP"],switch["Port"]),username=switch["Username"],password=switch["Password"],path_cert=CertPath,override=switch["Hostname"]) as gc:
            SetASN = [
                (
                    "/System/bgp-items/inst-items", #native model
                    {"asn":"{}".format(switch["ASN"])},
                )
            ]

            SetRouterID = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]".format(BGPName), #native model
                    {"rtrId":"{}".format(switch["RouterID"])},
                )
            ]
            
            SetAddressType = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]/af-items/DomAf-list".format(BGPName), #native model
                    {"type":"{}".format(switch["AddressType"])},
                )
            ]
            
            SetAddressFamilyNetwork = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]/af-items/DomAf-list[type={}]/prefix-items/AdvPrefix-list".format(BGPName,AddressType), #native model
                    {"addr":"{}".format(switch["AddressFamilyNetwork"])},
                )
            ]
            
            SetBGPNeighbor = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]/peer-items/Peer-list".format(BGPName), #native model
                    {"addr":"{}".format(switch["BGPNeighbor"])},
                )
            ]
            
            SetNeighborASN = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]/peer-items/Peer-list[addr={}]".format(BGPName,switch["BGPNeighbor"]), #native model
                    {"asn":"{}".format(switch["NeighborASN"])},
                )
            ]
            
            SetNeighborDescription = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]/peer-items/Peer-list[addr={}]".format(BGPName,switch["BGPNeighbor"]), #native model
                    {"name":"{}".format(switch["NeighborDescription"])},
                )
            ]
            
            SetUpdateValue = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]/peer-items/Peer-list[addr={}]".format(BGPName,switch["BGPNeighbor"]), #native model
                    {"kaIntvl":"{}".format(switch["UpdateValue"])},
                )
            ]
            
            SetHoldValue = [
                (
                    "System/bgp-items/inst-items/dom-items/Dom-list[name={}]/peer-items/Peer-list[addr={}]".format(BGPName,switch["BGPNeighbor"]), #native model
                    {"holdIntvl":"{}".format(switch["HoldValue"])},
                )
            ]
            
            SetNeighborAddressType = [
                (
                    "/System/bgp-items/inst-items/dom-items/Dom-list[name={}]/peer-items/Peer-list[addr={}]/af-items/PeerAf-list".format(BGPName,switch["BGPNeighbor"]), #native model
                    {"type":"{}".format(switch["NeighborAddressType"])},
                )
            ]
            
            
            print("Sending ASN...")
            gc.set(update=SetASN)
            print("Sending RouterID...")
            gc.set(update=SetRouterID)
            print("Sending Address Type...")
            gc.set(update=SetAddressType)
            print("Sending Address Family Network...")
            gc.set(update=SetAddressFamilyNetwork)
            print("Sending BGP Neighbor...")
            gc.set(update=SetBGPNeighbor)
            print("Sending BGP Neighbor ASN...")
            gc.set(update=SetNeighborASN)
            print("Sending BGP Neighbor Description...")
            gc.set(update=SetNeighborDescription)
            print("Sending Update Value...")
            gc.set(update=SetUpdateValue)
            print("Sending Hold Value...")
            gc.set(update=SetHoldValue)
            print("Sending Neighbor Address Type...")
            gc.set(update=SetNeighborAddressType)
            print("\n---------------------------------------\n")