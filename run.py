__author__ = 'Zamatica'
from multiprocessing import Process
from os import system
from update import update_timer


def start():
    print("")
    system("zamaticabat_base.py 1")
    print("")

if __name__ == '__main__':
    startup = Process(target=start)
    updates = Process(target=update_timer)
    startup.start()
    updates.start()
