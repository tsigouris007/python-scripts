#!/usr/bin/python

import sys, pexpect, argparse, os.path
from os import path
from pexpect import pxssh

def ssh_connect(host, usr, pwd):
    try:
        s = pxssh.pxssh()
        s.login(host, usr, pwd)
        s.sendline('uptime')
        s.prompt()
        print(s.before)
        s.logout()
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="The host you want to scan", type=str, required=True)
    parser.add_argument("--usr", help="The wordlist path containing usernames", type=str, required=True)
    parser.add_argument("--pwd", help="The wordlist path containing passwords", type=str, required=True)
    
    args = parser.parse_args()
    host = args.host
    usr = args.usr
    pwd = args.pwd

    if not path.exists(usr):
        print("Username file path does not exist.")
        sys.exit(2)

    if not path.exists(pwd):
        print("Password file path does not exist.")
        sys.exit(2)

    if not path.isfile(usr):
        print("Username file specified is not valid.")
        sys.exit(3)

    if not path.isfile(pwd):
        print("Password file specified is not valid.")
        sys.exit(3)

    try:
        usr_file = open(usr, 'r')
    except:
        print("Could not open username file.")
        sys.exit(4)

    try:
        pwd_file = open(pwd, 'r')
    except:
        print("Could not open password file.")
        sys.exit(4)

    usr_file.close()
    pwd_file.close()

    print(ssh_connect(host, "msfadmin", "msfadmin"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)