#!/usr/bin/python

import hashlib, sys, argparse

def md5(string):
    hashobject = hashlib.md5()
    hashobject.update(string.encode())
    return hashobject.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--string", help="The string you want to hash", type=str, required=True)
    
    args = parser.parse_args()
    string = args.string

    print(md5(string))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1) 