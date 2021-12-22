#!/usr/bin/python3

import sys, argparse, os, subprocess, random, platform, re

def get_random_char():
    return random.choice("abcdef0123456789")

def get_random_mac():
    mac = ""
    for i in range(0, 6):
        mac += get_random_char() + get_random_char() + ":"

    mac = mac[0:len(mac) - 1]
    return mac

def set_mac(iface, mac):
    try:
        subprocess.call(["sudo", "ifconfig", iface, "down"])
        subprocess.call(["sudo", "ifconfig", iface, "hw", "ether", mac])
        subprocess.call(["sudo", "ifconfig", iface, "up"])
        return True
    except:
        return False

def get_current_mac(iface):
    try:
        command = 'ifconfig ' + iface + ' | grep ether | grep -oE [0-9a-f:]{17}'
        out = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        return out
    except:
        return False

def validate_mac(mac):
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="The interface you want to change its MAC address. Default is eth0.", type=str, required=False)
    parser.add_argument("-c", help="Print your current MAC address. Halts any other processing.", action="store_true", required=False)
    parser.add_argument("-r", help="Generate a random MAC address to the specified interface. Does not work with --n.", action="store_true", required=False)
    parser.add_argument("-n", help="Manually change a MAC address to the specified interface. Does not work with --r.", type=str, required=False)

    args = parser.parse_args()

    system = platform.system()
    if system.upper() == "WINDOWS":
        print("Windows not supported")
        sys.exit(2)

    iface = 'eth0'
    if args.i != None:
        iface = args.i

    if not args.c:
        if args.r and args.n != None:
            print("Cannot use both flags -r and -n together.")
            sys.exit(3)

        if args.r:
            new_mac = get_random_mac()
            while not set_mac(iface, new_mac):
                pass

        if args.n != None:
            new_mac = args.n
            if validate_mac(new_mac):
                set_mac(iface, new_mac)
            else:
                print("Invalid MAC address.")
                sys.exit(4)

    print("Current MAC: " + get_current_mac(iface))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)
