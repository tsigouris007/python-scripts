#!/usr/bin/python

import socket, sys

def scanner(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex((host, port)):
        print("Open port")
    else:
        print("Closed port")

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    scanner(host, port)

if __name__ == "__main__":
    main()