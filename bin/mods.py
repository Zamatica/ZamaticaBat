# !/usr/bin/env python3
import ctypes, datetime, sqlite3, threading

from updates import follower_sub_update
import connections as con
import vars as variable


USERS = 'users/users.db'

send_message = con.send_message

run = 'Nothing Right Now.'

SendInput = ctypes.windll.user32.SendInput

# C structure redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class InputI(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", InputI)]


# Actual Functions
def press_key(key_code):

    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(key_code, 0x48, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key_code):

    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(key_code, 0x48, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def command_on():
    send_message("I am online and sending messages.")


def command_runtime():
    temp_now = datetime.datetime.now()
    calc = (80 ** 80) ** 80
    now = datetime.datetime.now()
    now -= temp_now
    send_message("Calculated " + str(calc)[0:5] + "... " + " in " + str(now))


def command_pong():
    send_message("Pong!")


def command_quote_add(quote_list):
    quotes = open('/systems/quotes.txt', 'a')
    quote = ' '.join(quote_list)
    quotes.write('"' + quote + '" ~ ' + variable.BROADCASTER[0].upper() + variable.BROADCASTER[1:20] + ", " + str(datetime.date.today().year))
    quotes.write("\n")
    quotes.close()
    send_message("Quote Added: " + quote)


def command_run_update(run_update):
    global run
    run = ' '.join(run_update)
    return run


def command_check(name):
    conn = sqlite3.connect(USERS)
    c = conn.cursor()
    name = name[0].lower()
    check = c.execute("SELECT * FROM users WHERE name LIKE ?", [str(name)])
    if str(name) in list(map(lambda x: x[0], check)):
        send_message(name[0].upper() + name[1:50] + " is in the USERS.")
        conn.commit()
        conn.close()
        return True
    else:
        send_message(name[0].upper() + name[1:50] + " is not in the USERS.")
        conn.commit()
        conn.close()
        return False


def command_add(name):
    conn = sqlite3.connect(USERS)
    c = conn.cursor()
    name_str = name[0].lower()
    punc = name_str[0].upper() + name_str[1:50]
    if command_check(name) is False:
        c.execute("INSERT OR IGNORE INTO users (name) VALUES (?);", [name_str])
        send_message(punc + " added.")
    conn.commit()
    conn.close()


# Viewers
def threading_timer():

    threading.Timer(variable.UPDATE, threading_timer)
    conn = sqlite3.connect(USERS)
    c = conn.cursor()

    global user_mods
    user_mods = list(map(lambda x: x[0], c.execute("SELECT * from users WHERE mod = 1;")))
    conn.commit()
    conn.close()

    follower_sub_update()
    print("-- SYSTEM: Mods Updated.")

    return user_mods


def command_play_pause():
    if variable.MUSIC_ENABLED == 1:
        try:
            press_key(0xB3)
            release_key(0xB3)
        except NameError:
            print("-- ERROR: NameError on !play")


def command_play_next():
    if variable.MUSIC_ENABLED == 1:
        try:
            press_key(0xB0)
            release_key(0xB0)
        except NameError:
            print("-- ERROR: NameError on !next")


def command_play_pre():
    if variable.MUSIC_ENABLED == 1:
        try:
            press_key(0xB1)
            release_key(0xB1)
        except NameError:
            print("-- ERROR: NameError on !prev")


def mod_commands():
    send_message("Moderator Loaded.")

