import threading
import time
import sys
import keyboard
import easygui

shutdown = False
cancel = ""


def wait_for_enter():
    print("Hit Enter to quit.")
    input()
    global shutdown
    shutdown = True


threading.Thread(target=wait_for_enter).start()
print("a")
try:
    while True:
        print(3)
        if shutdown is True:
            raise SystemExit
except SystemExit:
    print("Program Ended")
