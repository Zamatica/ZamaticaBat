# !/usr/bin/env python3
from multiprocessing import Process
from os import system

from users.updates import update_timer

with open("bin/systems/connection.txt", 'w'):
    pass


def start():
    print("")
    system("python bin/base.py")
    print("")


if __name__ == '__main__':
    startup = Process(target=start)
    updates = Process(target=update_timer)
    startup.start()
    updates.start()
