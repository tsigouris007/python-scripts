#!/usr/bin/python3

import hashlib, sys, argparse, itertools, string, time
try:
    from itertools import imap
except ImportError:
    imap=map # For Python 3

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
                        help="The hash string you want to bruteforcing",
                        type=str,
                        required=True)
    parser.add_argument("--method",
                        help="The hash method you want use while bruteforcing. Available md5, sha1, sha256, sha512",
                        choices=['md5','sha1','sha256','sha512'],
                        type=str,
                        required=True)
    parser.add_argument("--minlength",
                        help="The minimum length of the word you want to generate while bruteforcing. Default is 1.",
                        required=False)
    parser.add_argument("--maxlength",
                        help="The maximum length of the word you want to generate while bruteforcing. Default is 16.",
                        required=False)
    parser.add_argument("--chars",
                        help="The characters you want to generate while bruteforcing. Default are all printable characters.",
                        required=False)
    
    args = parser.parse_args()
    hashstr = args.hash
    method = args.method

    minlength = 1
    if args.minlength != None:
        minlength = int(args.minlength)

    maxlength = 16
    if args.maxlength != None:
        maxlength = int(args.maxlength)

    chars = string.printable
    if args.chars != None:
        chars = args.chars

    done = False
    for i in range(minlength, maxlength + 1):
        for word in imap(''.join, itertools.product(chars, repeat=int(i))):
            if hasher(method, word) == hashstr:
                print("Cracked hash: %s (%s)" % (hashstr, word))
                done = True
                break

    if not done:
        print("Failed to crack.")

if __name__ == "__main__":
    try:
        start_time = time.time()
        main()
        end_time = time.time()
        print("Elapsed: ", round(end_time - start_time, 3), "seconds")
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)
