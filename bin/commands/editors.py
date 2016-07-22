# !/usr/bin/env python3
from sys import exit
import os

import systems.connections as con

send_message = con.send_message


def command_timeout(name, time):
    send_message('/timeout ' + name + ' ' + time)


def command_off():
    send_message("Logging Off...")
    print("")
    print("-- SYSTEM: Commands Stopped.")
    os.remove("bin/systems/connection.txt")
    exit()


def editor_command():
    send_message("Editor Loaded.")