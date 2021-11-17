#!/usr/bin/python3

import argparse
from scapy.all import *
import sys

def syn(src, sport, dst, dport, msg):
  ip_layer = IP(src=src, dst=dst)
  tcp_layer = TCP(sport=sport, dport=dport)
  raw_layer = Raw(load=msg)
  packet = ip_layer/tcp_layer/raw_layer
  print("Sending from %s:%i to %s:%i (%s)" % (src, sport, dst, dport, msg))
  send(packet)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--src", type=str, required=True, help="The source IP.")
  parser.add_argument("--sport", type=int, required=False, default=1234, help="The source IP port. Default: 1234")
  parser.add_argument("--dst", type=str, required=True, help="The destination IP.")
  parser.add_argument("--dport", type=int, required=False, default=80, help="The destination IP port. Default: 80")
  parser.add_argument("--count", type=int, required=False, default=1, help="How many times to send your packet. Default: 1")
  parser.add_argument("--message", type=str, required=False, default="", help="The message you wanna send.")

  args = parser.parse_args()

  src = args.src
  sport = args.sport
  dst = args.dst
  dport = args.dport
  msg = args.message
  cnt = args.count

  for i in range(0, cnt):
    syn(src, sport, dst, dport, msg)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("Interrupted")
    sys.exit(1)