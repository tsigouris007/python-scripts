#!/usr/bin/python

import hashlib, sys, argparse
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
		
def store_session(index):
    try:
        session = open(".session", "w")
        session.write(str(index))
        session.close()
        return True
    except:
        return False

def restore_session():
    try:
        session = open(".session", "r")
        line = session.readline().strip()
        return int(line)
    except Exception:
        return False

def reset_session():
    try:
        session = open(".session", "w")
        session.write("0")
        session.close()
        return True
    except:
        return False

def md5(string):
    hashobject = hashlib.md5()
    hashobject.update(string.encode())
    return hashobject.hexdigest()

def sha1(string):
    hashobject = hashlib.sha1()
    hashobject.update(string.encode())
    return hashobject.hexdigest()

def sha256(string):
    hashobject = hashlib.sha256()
    hashobject.update(string.encode())
    return hashobject.hexdigest()

def sha512(string):
    hashobject = hashlib.sha512()
    hashobject.update(string.encode())
    return hashobject.hexdigest()

def hasher(method, string):
    if method == 'md5':
        return md5(string)
    elif method == 'sha1':
        return sha1(string)
    elif method == 'sha256':
        return sha256(string)
    elif method == 'sha512':
        return sha512(string)
    else:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hash",
                        help="The hash string you want to crack",
                        type=str,
                        required=True)
    parser.add_argument("--method",
                        help="The hash method you want use while cracking. Available md5, sha1, sha256, sha512",
                        choices=['md5','sha1','sha256','sha512'],
                        type=str,
                        required=True)
    parser.add_argument("--list",
                        help="The wordlist you want to use while cracking.",
                        required=True)
    parser.add_argument("--rst",
                        help="Flag to reset your session file",
                        action="store_true",
                        required=False)
    
    args = parser.parse_args()
    hashstr = args.hash
    method = args.method
    wlist = args.list
    rst = args.rst

    if not path.exists(wlist):
        print("Wordlist file path does not exist.")
        sys.exit(2)

    if not path.isfile(wlist):
        print("Wordlist file specified is not valid.")
        sys.exit(3)

    if rst:
        reset_session()

    pos = 0
    if not check_session():
        if not create_session():
            print("Failed to create new session.")
            sys.exit(4)
    else:
        if not rst:
            print("Restoring last session.")
            pos = restore_session()

    f = open(wlist, "r")
    idx = 0
    done = False
    for line in f:
        idx += 1
        if idx < pos:
            continue
        else:
            pos = 0
        
        line = line.strip()
        if hasher(method, line) == hashstr:
            print("Cracked hash: %s (%s)" % (hashstr, line))
            done = True
            break

        if not store_session(idx):
                print("Could not save current session.")
                sys.exit(4)

    f.close()

    if not done:
        print("Failed to crack.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1) 