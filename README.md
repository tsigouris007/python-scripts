# A collection of my custom Python Scripts

Everything seems pretty self explanatory. There scripts are standalone, so duplicates of code are unavoidable.

Some extra packages may need to be installed in order for these to work.

There are more sophisticated tools out there that can perform the same functionalities or even better but coding custom tools is always a good mental exercise. You can also get an idea of how these tools, you might be using, work.

**Working with Python >= 3 version**

## Port Scanner

Usage examples:

`python3 portscan.py --host 192.168.1.1 --port 80`

*To specify multiple ports*

`python3 portscan.py --host 192.168.1.1 --port 21,22,25,80`

*To specify a range of ports*

`python3 portscan.py --host 192.168.1.1 --port 1-1000`

*Returns a table of results similar to the nmap.*

## SSH Bruteforce

Usage examples:

`python3 sshbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt`

*To specify another SSH service port*

`python3 sshbrute.py --host 192.168.1.1 --port 22 --usr usersfile.txt --pwd passfile.txt`

*To reset your session before bruteforce*

`python3 sshbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt --rst`

*Returns a successful user:pass combination.*

## FTP Bruteforce

Usage examples:

`python3 ftpbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt`

*To specify another FTP service port*

`python3 ftpbrute.py --host 192.168.1.1 --port 21 --usr usersfile.txt --pwd passfile.txt`

*To try anonymous login too on top of wordlist bruteforce*

`python3 ftpbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt --anon`

*To reset your session before bruteforce*

`python3 ftpbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt --rst`

*Returns a successful user:pass combination.*

## Hash Cracker

**Available methods md5, sha1, sha256, sha512**

`python hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5 --list userlist.txt`

*Returns a successful plaintext string if cracked*

## Hash Bruteforce

**Available methods md5, sha1, sha256, sha512**

`python3 hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5`

*Specify a minimum or maximum length for bruteforcing*

`python3 hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5 --minlength 4 --maxlength 8`

*Specify a custom character set for bruteforcing*

`python3 hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5 --minlength 4 --maxlength 8 --chars ABCDabcd1234!@#`

*Returns a successful plaintext string if cracked*

## Mac Changer

*Display your current MAC Address*

`python3 hashcracker.py --c`

*Specify an interface*

`python3 hashcracker.py --c --i eth0`

*Generate a Random MAC Address on a specified interface (optional)*

`python3 hashcracker.py --r --i eth0`

*Manually set a MAC Address on a specified interface (optional)*

`python3 hashcracker.py --n 00:11:22:33:44:55 --i eth0`