# !/usr/bin/env python3
from multiprocessing import Process
from os import system

from updates import update_timer

with open("systems/connection.txt", 'w'):
    pass


def start():
    print("")
    system("base.py 1")
    print("")


if __name__ == '__main__':
    startup = Process(target=start)
    updates = Process(target=update_timer)
    startup.start()
    updates.start()
