#!/usr/bin/python3

from NMtcpdump import find_macaddr
from NMdhcpserver import configure_dhcpv4
from NMsnmp.py import get_interface_details

def main():
    r2r3_macaddr_dict = find_macaddr()

    configure_dhcpv4(r2r3_macaddr_dict)

    get_interface_details()

if __name__ == "__main__":
    main()