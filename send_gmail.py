#!/usr/bin/python3

import smtplib, argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-e", "--email", type=str, required=True, help="Your login email.")
  parser.add_argument("-p", "--pwd", type=str, required=True, help="Your login password.")
  parser.add_argument("-f", "--frm", type=str, required=False, help="The email from.")
  parser.add_argument("-b", "--body", type=str, required=False, help="The email body.")
  args = parser.parse_args()

  email = args.email
  pwd = args.pwd

  if args.frm == '' or args.frm == None:
    frm = email
  else:
    frm = args.frm

  if args.body == '' or args.body == None:
    body = "Hello world."
  else:
    body = args.body

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(email, pwd)
  server.sendmail(frm, email, body)
  server.quit()

if __name__ == "__main__":
  main()