# A collection of my custom Python Scripts

Everything seems pretty self explanatory.
Some extra packages may need to be installed in order for these to work.

**Working with Python >= 3 version**

## Port Scanner

Usage examples:

`python3 portscan.py --host 192.168.1.1 --port 80`

`python3 portscan.py --host 192.168.1.1 --port 21,22,25,80`

`python3 portscan.py --host 192.168.1.1 --port 1-1000`

*Returns a table of results similar to the nmap.*

## SSH Bruteforce

Usage examples:

`python3 sshbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt`

`python3 sshbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt --rst` *To reset your session*

*Returns a successful user:pass combination.*