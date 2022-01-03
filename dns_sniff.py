#!/usr/bin/python3

import sys, argparse
import scapy.all as scapy

def get_dns(packet):
    if packet.haslayer(scapy.DNS):
        dnsrr = False
        packet_str = "".join(map(chr, bytes(packet.getlayer(scapy.DNS))))
        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
        summary = packet[scapy.DNS].summary()
        if packet.haslayer(scapy.DNSRR):
            dnsrr = True
        print(ip_src, "->", ip_dst, ":", summary, ", DNSRR: ", dnsrr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="The interface you want to sniff.", default="eth0", type=str, required=False)
    args = parser.parse_args()

    interface = args.i

    try:
        print("Sniffing DNS traffic...")
        scapy.sniff(iface=interface, store=False, prn=get_dns)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)

if __name__ == "__main__":
    main()
