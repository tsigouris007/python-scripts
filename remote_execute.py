#!/usr/bin/env python3
import paramiko
from paramiko import AutoAddPolicy
import os
import argparse
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ssh_remote_execute(host, user, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy)
        ssh.load_system_host_keys()
        ssh.connect(host, username=user, look_for_keys=False)
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        for line in stdout.readlines():
            print(bcolors.OKGREEN + bcolors.BOLD + user+"@"+host+ "~$ " + bcolors.ENDC + line, end='')
        ssh.close()
    except Exception as e:
        print(e)

def read_file(infile):
    out = []
    f = open(infile, 'r')
    lines = f.readlines()
    for l in lines:
        if l and l != '' and l != '\n' and l != '\r\n':
            out.append(l.strip())
    f.close()
    return out

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--host', type=str, required=True, help='The hostname you want to connect. You can specify multiple delimited by comma or a file.')
    parser.add_argument('-u', '--user', type=str, required=False, default=os.getlogin(), help='The user you want to connect as. Default your current one.')
    parser.add_argument('-c', '--cmd', type=str, required=False, default="hostname", help='The command you want to run on the remote machine. You can also specify a file.')
    args = parser.parse_args()

    fhost = args.host
    fcmd = args.cmd
    user = args.user

    if os.path.isfile(fhost):
        hosts = read_file(fhost)
    else:
        hosts = fhost.split(',')

    cmd = []
    if os.path.isfile(fcmd):
        cmd = read_file(fcmd)
    else:
        cmd.append(fcmd)

    for h in hosts:
        for c in cmd:
            print(f"{bcolors.OKBLUE}Connecting to host:{bcolors.ENDC} ", h, f" {bcolors.OKBLUE}executing:{bcolors.ENDC} ", c)
            ssh_remote_execute(h, user, c)

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)
