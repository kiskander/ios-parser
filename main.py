#!/usr/bin/env python3
from ciscoconfparse import CiscoConfParse
from netaddr import *

parse = CiscoConfParse('device.conf')

# Return a list of all interfaces
intfs = parse.find_objects(r"^interface")

def translate_netmask(ip):
    ip = IPNetwork(ip)
    return ip.netmask, ip.ip

# For each interface above, print out relevant information...
for obj in intfs:
    print("-----")

    # Find the interface mode
    intf_mode = obj.re_match_iter_typed(r'^\s*(switchport).*$', default='routed')

    # Find the IP address by iterating over all children of this parent...
    ip_addr = obj.re_match_iter_typed(r'ip\saddress\s(\S+)')

    ip_mask = obj.re_match_iter_typed(r'ip\saddress\s\S+\s+(\S+)')

    mask, ip = translate_netmask(ip_addr)
    # Print out what we found...
    print("Object: {0}".format(obj))
    print("  Interface config line: {0}".format(obj.text))
    print("  Interface mode: {0}".format(intf_mode))
    print("  IP address: {0} {1}".format(ip, mask))


