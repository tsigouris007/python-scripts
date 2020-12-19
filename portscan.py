#!/usr/bin/python

import socket, sys, argparse, subprocess, platform
from termcolor import colored
from datetime import datetime
from threading import *
import time
from tabulate import tabulate

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

def scanner(host, port):
    #socket.setdefaulttimeout(30)
    banner = ""
    state = ""
    sock_type = "tcp"
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((host, port))
            banner = str(sock.recv(4096).decode("utf-8")).strip()
        except:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            request = "HEAD / HTTP/1.1\r\nHost:%s\r\n\r\n" % host
            sock.send(request.encode())
            response = sock.recv(4096)
            banner = cleanlist(repr(response.decode("utf-8")).replace("\'", "").split("\\r\\n"))
        state = "open"
    except:
        banner = None
        state = "closed"
    finally:
        sock.close()
    return (port, sock_type, state, banner)

def cleanlist(list):
    while("" in list):
        list.remove("")
    return list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="The host you want to scan", type=str)
    parser.add_argument("--port", help="The port you want to scan. You can use a single port, a comma delimited port list such as 22,25,80 or a port range such as 1-1000", type=str)
    
    args = parser.parse_args()
    host = args.host
    ports = args.port

    printstarthost(host)
    
    if pingtest(host):
        print("Host %s responds to ping." % host)
    else:
        print("Host %s does not respond to ping." % host)

    ip = getIP(host)
    if ip != host:
        print("Host %s resolves to %s" % (host, ip))

    results = []

    try:
        p = int(ports)

        start_time = time.time()
        (rport, rsock_type, rstate, rbanner) = scanner(host, int(p))
        result = [rport, rsock_type, rstate, rbanner]
        results.append(result)
        end_time = time.time()
    except:
        if ("," in ports and "-" in ports):
            print("Invalid port option")
            sys.exit(2)
        
        if ("," in ports):
            portlist = ports.split(",")
            portlist = cleanlist(portlist)

            start_time = time.time()
            for p in portlist:
                (rport, rsock_type, rstate, rbanner) = scanner(host, int(p))
                result = [rport, rsock_type, rstate, rbanner]
                results.append(result)
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
            
            start_time = time.time()
            for p in range(startport, endport + 1):
                (rport, rsock_type, rstate, rbanner) = scanner(host, int(p))
                result = [rport, rsock_type, rstate, rbanner]
                results.append(result)
            end_time = time.time()

        else:
            print("Invalid port option")
            sys.exit(2)

    print(tabulate(results, headers=["PORT", "TYPE", "STATE", "BANNER"]))
    print("Elapsed: ", round(end_time - start_time, 3), "seconds")
    printendhost(host)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)
