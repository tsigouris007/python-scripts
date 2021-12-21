#!/usr/bin/python3

import sys, socket
from struct import *

PACKET_SIZE = 65535

def eth_addr(p):
    a = str(hex(p[0])).replace('0x','')
    b = str(hex(p[1])).replace('0x','')
    c = str(hex(p[2])).replace('0x','')
    d = str(hex(p[3])).replace('0x','')
    e = str(hex(p[4])).replace('0x','')
    f = str(hex(p[5])).replace('0x','')
    addr = "%s:%s:%s:%s:%s:%s" % (a, b, c, d, e, f)
    return addr

def create_socket():
    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        return s
    except:
        print("Could not create socket.")
        sys.exit(1)

def main():
    s = create_socket()

    try:
        print('+' + '-' * 50 + '+')
        print('| Dst MAC ' + ' ' * 11 + '| Src MAC ' + ' ' * 11 + '| Proto  |')
        while True:
            p = s.recvfrom(PACKET_SIZE)
            p = p[0]
            eth_header = p[:14]
            eth = unpack('!6s6sH', eth_header)
            eth_proto = socket.ntohs(eth[2])
            dst_mac = eth_addr(p[0:6])
            src_mac = eth_addr(p[6:12])

            print('| %s | %s | %s |' % (dst_mac.ljust(18), src_mac.ljust(18), str(eth_proto).ljust(6)))
    except KeyboardInterrupt:
        print('+' + '-' * 50 + '+')
        sys.exit(1)

if __name__ == "__main__":
    main()
