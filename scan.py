#!/usr/bin/python

import socket, sys, argparse, subprocess, platform
from termcolor import colored
from datetime import datetime
from threading import *
import time

MAXPORT = 65535
MINPORT = 0

def getIP(host):
    try:
        ip = socket.gethostbyname(host)
    except:
        return host
    return ip

def pingtest(host):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', host), shell=True)
    except:
        return False
    return True 

def printstarthost(host):
    now = datetime.now()
    print("Starting host scan on %s at %s" % (host, now))

def printendhost(host):
    now = datetime.now()
    print("Finished host scan on %s at %s" % (host, now))

def printheader():
    print("PORT\t\tSTATE")

def scanner(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(2)
        sock.connect((host, port))
        print(colored("%d\\tcp\t\topen" % port, "green"))
    except:
        print(colored("%d\\tcp\t\tclosed" % port, "red"))
    finally:
        sock.close()

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
    screen_lock = Semaphore(value=1)

    printstarthost(host)
    
    if pingtest(host):
        print("Host %s responds to ping." % host)
    else:
        print("Host %s does not respond to ping." % host)

    ip = getIP(host)
    if ip != host:
        print("Host %s resolves to %s" % (host, ip))

    try:
        p = int(ports)

        printheader()
        start_time = time.time()
        #t = Thread(target=scanner, args=(host, int(p)))
        #t.start()
        scanner(host, p)
        end_time = time.time()

    except:
        if ("," in ports):
            portlist = ports.split(",")
            portlist = cleanportlist(portlist)

            printheader()
            start_time = time.time()
            for p in portlist:
                #t = Thread(target=scanner, args=(host, int(p)))
                #t.start()
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
                #t = Thread(target=scanner, args=(host, int(p)))
                #t.start()
                scanner(host, int(p))
            end_time = time.time()

        else:
            print("Invalid port option")
            sys.exit(2)

    print("Elapsed: ", round(end_time - start_time, 3), "seconds")
    printendhost(host)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)