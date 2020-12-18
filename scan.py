#!/usr/bin/python

import socket, sys, argparse
from termcolor import colored
from datetime import datetime
from threading import *
import time

MAXPORT = 65535
MINPORT = 0

def printstarthost(host):
    now = datetime.now()
    print("Starting host scan on %s at %s" % (host, now))

def printendhost(host):
    now = datetime.now()
    print("Starting host scan on %s at %s" % (host, now))

def printheader():
    print("PORT\t\t\tSTATE")

def scanner(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(2)
    if sock.connect_ex((host, port)):
        print(colored("%d\\tcp\t\t\topen" % port, "green"))
    else:
        print(colored("%d\\tcp\t\t\tclosed" % port, "red"))

def cleanportlist(portlist):
    while("" in portlist):
        portlist.remove("")
    return portlist

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="The host you want to scan", type=str)
    parser.add_argument("--port", help="The port you want to scan. You can use a single port, a comma delimited port list such as 22,25,80 or a port range such as 1-1000", type=str)
    
    args = parser.parse_args()
    host = args.host
    ports = args.port

    printstarthost(host)

    try:
        p = int(ports)

        printheader()
        start_time = time.time()
        scanner(host, p)
        end_time = time.time()

    except:
        if ("," in ports):
            portlist = ports.split(",")
            portlist = cleanportlist(portlist)

            printheader()
            start_time = time.time()
            for p in portlist:
                scanner(host, int(p))
            end_time = time.time()

        elif ("-" in ports):
            portlist = ports.split("-")

            if (portlist[0] == ""):
                startport = MINPORT
            else:
                startport = int(portlist[0])
            if (portlist[1] == ""):
                endport = MAXPORT
            else:
                endport = int(portlist[1])
            if startport > endport:
                print("Invalid port range")
                sys.exit(3)
            
            printheader()
            start_time = time.time()
            for p in range(startport, endport):
                scanner(host, int(p))
            end_time = time.time()

        else:
            print("Invalid port option")
            sys.exit(2)

    print("Elapsed: ", round(end_time - start_time, 3))
    printendhost(host)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)