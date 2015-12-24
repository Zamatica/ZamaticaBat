__author__ = 'Zamatica'

# !/usr/bin/env python3

import socket
import datetime
import sqlite3
import threading
import json
import random
import linecache
import re
import ctypes
import subprocess
from update import return_x, mod_update, viewer_update
from sys import exit
from time import sleep


# --------------------------------------------- Start Settings ---------------------------------------------------- #

with open("vars.json") as file:
    VARS = json.load(file)

HOST = VARS["connection"]["HOST"]            # Host
PORT = VARS["connection"]["PORT"]            # Port
CHAN = VARS["connection"]["CHAN"]            # # + Your Twitch Username
NICK = VARS["connection"]["NICK"]            # Your Bot's Twitch username
PASS = VARS["connection"]["PASS"]            # http://www.twitchapps.com/tmi/ -- Google This.

PORT = int(PORT)

# User Variables

# Variables -- 1 = On/0 = Off

start = datetime.datetime.now()

USER = VARS["connection"]["CHAN"][1:100]

TIMEZONE = VARS["variables"]["TIMEZONE"]  # Change to Yours

MEDIA_ENABLED = int(VARS["variables"]["MEDIA_ENABLED"])  # Show title/media every time. Default 0

TITLE = VARS["variables"]["TITLE"]   # Update Every Stream - Shown every TITLE_SHOWN seconds, default 75.0
TITLE_SHOWN = float(VARS["variables"]["TITLE_SHOWN"])

SOCIAL_MEDIA = VARS["variables"]["SOCIAL_MEDIA"]  # Add info here - Shown every MEDIA_SHOWN seconds, default 180.0
MEDIA_SHOWN = float(VARS["variables"]["MEDIA_SHOWN"])


BROADCAST_ENABLED = int(VARS["variables"]["BROADCAST_ENABLED"])

BROADCAST_SHOWN = float(VARS["variables"]["BROADCAST_SHOWN"])

BROADCAST = VARS["variables"]["BROADCAST"]


TIMEOUT_TIME = int(VARS["variables"]["TIMEOUT_TIME"])   # Timeout time for offenders, default 45.0

TIMEOUT_LIMIT = int(VARS["variables"]["TIMEOUT_LIMIT"])  # Limit for number of offences, default 3

UPDATE = float(VARS["variables"]["UPDATE"])   # How often user list is updated

SUBS = int(VARS["variables"]["SUBS"])
SUB_OAUTH = VARS["variables"]["SUB_OAUTH"]

# VARIABLE = {}  <-- {'word', 'word2', 'word3'} can have more than 3

BANNED_WORDS = VARS["variables"]["BANNED_WORDS"]   # ... add what ever you like, no spaces, ALL LOWERCASE


BROADCASTER = VARS["variables"]["BROADCASTER"]  # YOU, Editors, and anyone you trust with this, ALL LOWERCASE

# Currency
CURRENCY_ENABLED = int(VARS["variables"]["CURRENCY_ENABLED"])  # Reward for spending time, default 0

CURRENCY_MINUS = int(VARS["variables"]["CURRENCY_MINUS"])  # Punishment for offenses, default 20. Want to disable? make 0

CURRENCY_VALUE = int(VARS["variables"]["CURRENCY_VALUE"])  # Set value of currency, default 15

UPDATE_CURRENCY = int(VARS["variables"]["UPDATE_CURRENCY"])  # Time for currency to be added, in seconds, default 3600 (1 hour)

# BETA Features
WINDOW_SIZE = int(VARS["variables"]["WINDOW_SIZE"])

MUSIC_ENABLED = int(VARS["variables"]["MUSIC_ENABLED"])


# End User Variables

# System Variables
DATABASE = 'users.db'

connect_bot = 0

run = 'Nothing right now.'

user_mods = {}
user_subs = {}
user_fols = {}


# --------------------------------------------- End Settings ------------------------------------------------------- #


# --------------------------------------------- Start Functions ---------------------------------------------------- #

def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def whisper(user, msg):
    send_message(CHAN, ("/w " + user + " " + msg))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


# --------------------------------------------- End Functions ------------------------------------------------------ #


# --------------------------------------------- Start Helper Functions --------------------------------------------- #

def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result

    # ---- Commands ---- #


# Begin Code
def parse_message(msg):
    if BOT_ENABLED == 1:
        if len(msg) >= 1:
            msg = msg.split(' ')

            for i in msg[0:50]:
                if i in BANNED_WORDS:
                    command_timeout_auto_1(sender)
                    command_nowhere_auto(sender)
                break

            msg_join = ' '.join(msg)

            if msg_join.isupper():
                if sender in user_mods:
                    command_null()
                else:
                    send_message(CHAN, "We can hear you just fine " + sender + ".")

            options = {}
            options_3 = {}
            options_mod = {}
            options_mod_1 = {}
            options_mod_4 = {}
            options_broad = {}

            if sender is not '':

                options = {

                    '!test': command_test,
                    '!uptime': command_uptime,
                    '!time': command_time,
                    '!help': command_help,
                    '!stats': command_stats,
                    '!coin': command_null,
                    '!quote': random_quote,
                    '!run': command_run,


                    'FrankerZ': frankerz,
                }

                options_3 = {

                    '!purchase': command_purchase,

                }

                options_mod = {
                    '!on': command_null,
                    '!admin': command_null,
                    '!ping': command_null,
                    '!con': command_null,

                    '!pong': command_pong,

                }

                options_broad = {
                    '!off': command_null
                }

            if sender in user_mods or sender in BROADCASTER:

                options_mod_4 = {

                    '!coin': command_coin,

                }

                options_mod = {

                    # Commands give to Mods and Broadcaster from USER_MODS and BROADCASTER
                    '!on': command_on,
                    '!admin': command_admin,
                    '!runtime': command_runtime,
                    '!ping': command_pong,
                    '!update': update_command,
                    '!p': command_play_pause,
                    '!pn': command_play_next,
                    '!pp': command_play_pre,

                }

                options_mod_1 = {

                    '!quoteadd': command_quote_add,
                    '!runset': command_run_update,
                    '!mod': promote_mod,
                    '!check': command_check,
                    '!add': command_add

                }

            if sender in BROADCASTER:

                options_broad = {

                    # Commands only given to BroadCaster from BROADCASTER VARIABLE
                    '!off': command_off,
                    '!broad': command_start_all,
                    '!conn': conntest,
                    '!mods': send_mod

                }

            # Ignore Me
            if msg[0] in options:
                try:
                    options[msg[0]]()
                except KeyError:
                    print("-- SYSTEM: KeyError?")
            if msg[0] in options_mod:
                try:
                    options_mod[msg[0]]()
                except KeyError:
                    print("-- SYSTEM: KeyError?")
            if msg[0] in options_broad:
                try:
                    options_broad[msg[0]]()
                except KeyError:
                    print("-- SYSTEM: KeyError?")
            # Placeholder

            elif msg[0] in options_mod_1:
                try:
                    options_mod_1[msg[0]](msg[1:50])
                except KeyError:
                    # Argument is not present
                    send_message(CHAN, 'KeyError: One parameter is required.')
                    pass

            elif msg[0] in options_3:
                try:
                    print("' " + str(msg[2]) + " '")
                    if '' in msg[2:50] and len(msg[2:50]) == 1:
                        quantity = ['1', '']
                        options_3[msg[0]](msg[1], quantity)
                    else:
                        options_3[msg[0]](msg[1], msg[2:50])
                except KeyError:
                    # Key is not present
                    send_message(CHAN, sender + ', two parameter are required. !purchase <item> <quantity>')
                    pass

            elif msg[0] in options_mod_4:
                try:
                    if '' in msg[1] and len(msg[1]) == 1:

                        send_message(CHAN, "Error, QUANTITY not filled. !coin <cmd> <quantity> <name>. Or use two-digits.")
                        options_mod_4[msg[0]]('help', '01', '01')
                    try:
                        if msg[2] == '':
                            send_message(CHAN, "Need Amount. !coin <cmd> <amount> <name>")
                        else:
                            try:
                                if msg[3] == '':
                                    send_message(CHAN, "Need Name. !coin <cmd> <amount> <name>")
                                else:
                                    options_mod_4[msg[0]](msg[1], msg[2], msg[3])
                            except IndexError:
                                options_mod_4[msg[0]]('help', '01', '01')
                                pass
                    except IndexError:
                        options_mod_4[msg[0]]('help', '01', '01')
                        pass
                except KeyError:
                    # Key is not present
                    send_message(CHAN, sender + ', three parameters are required. !coin <cmd> <quantity> <name>')
                    pass

# --------------------------------------------- End Helper Functions ----------------------------------------------- #

# -------------------------------------------------- Start ctypes -------------------------------------------------- #

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

# --------------------------------------------------- End ctypes --------------------------------------------------- #

# --------------------------------------------- Start Command Functions -------------------------------------------- #


# -------------- #
# ---- User ---- #
# -------------- #
def command_nowhere():
    if sender not in user_mods:
        print(sender + " has made on offense.")

    return sql_timeout(sender)


def command_nowhere_auto(name):

    print(name + " has made on offense.")

    return sql_timeout(name)


def command_null():
    a = 0
    a += 1
    return a


def command_help():
    send_message(CHAN, 'There is !help, !ping, !uptime, !time, !stats, !run, !coin, and !test.')
    if sender in user_mods:
        send_message(CHAN, 'Mod: !runset, !on, !admin, !runtime, !ping, !addquote, !p(n/p), and !update.')


def command_nonadmin_off():
    send_message(CHAN, "No. You are not the broadcaster, " + sender + ".")


def command_uptime():
    now = datetime.datetime.now()
    timepass = now - start

    total_seconds = int(timepass.total_seconds())
    hours, remainder = divmod(total_seconds, 60*60)
    minutes, seconds = divmod(remainder, 60)

    send_message(CHAN, '{} hrs {} mins {} secs'.format(hours, minutes, seconds))


def command_time():
    now = datetime.datetime.now()
    send_message(CHAN, str(now)[0:19] + " " + TIMEZONE)


def command_test():
    send_message(CHAN, 'Testing stuff')  # command to test if working, can use !on


def command_pong():
    send_message(CHAN, "Pong!")


def command_runtime():
    temp_now = datetime.datetime.now()
    calc = (80 ** 80) ** 80
    now = datetime.datetime.now()
    now -= temp_now
    send_message(CHAN, "Calculated " + str(calc)[0:5] + "... " + " in " + str(now))


def command_purchase(item, quantity):

    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    name = sender
    if CURRENCY_ENABLED == 1:

        if item == 'timeout':
            item_buy = 'timeout'
            for timeout in c.execute("SELECT ? FROM tableOut WHERE name LIKE ?", [item_buy, name]):
                timeouts = timeout[0]
                if timeouts > 0:
                    for stats in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name]):
                        if stats[0] >= (CURRENCY_VALUE*4)*int(quantity[0]):
                            c.execute("UPDATE tableOut SET currency = currency - ? WHERE name = ?;", [CURRENCY_VALUE*4*int(quantity[0]), name])
                            c.execute("UPDATE tableOut SET timeout = timeout - ? WHERE name = ?;", [quantity[0], name])
                            conn.commit()
                            for stats_new in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name]):
                                for timeout_new in c.execute("SELECT ? FROM tableOut WHERE name LIKE ?", [item_buy, name]):
                                    send_message(CHAN, "{}, you have purchased a warning removed. You now have ${} and {} timeouts".format(name, stats_new[0], timeout_new[0]))
                                    break
                                break
                        else:
                            send_message(CHAN, name + ", you do not have enough.")
                        break
                else:
                    send_message(CHAN, name + ", you have 0 timeouts.")
                break

    else:
        send_message(CHAN, "Currency Disabled")

    conn.commit()
    conn.close()


def command_coin(cmd, amount, name):

    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    name_0 = name
    amount_0 = amount

    if CURRENCY_ENABLED == 1:
            add = {'add', 'plus', '+'}
            sub = {'sub', 'subtract', '-'}

            if cmd == 'help':
                send_message(CHAN, "!coin has add, subtract, and set. !coin <cmd> <amount> <name>")

            elif cmd in add:
                c.execute("UPDATE tableOut SET currency = currency + (?) WHERE name LIKE (?)", [amount_0, name_0])
                conn.commit()
                for value in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name_0, ]):
                    send_message(CHAN, name_0 + " now has $" + str(value[0]) + ".")

            elif cmd in sub:
                c.execute("UPDATE tableOut SET currency = currency - ? WHERE name LIKE ?", [amount_0, name_0])
                conn.commit()
                for value in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name_0, ]):
                    send_message(CHAN, name_0 + " now has $" + str(value[0]) + ".")

            elif cmd == 'set':
                c.execute("UPDATE tableOut SET currency = ? WHERE name LIKE ?", [amount_0, name_0])
                conn.commit()
                for value in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name_0, ]):
                    send_message(CHAN, name_0 + " now has $" + str(value[0]) + ".")

    else:
        send_message(CHAN, "Currency Disabled.")

    conn.close()


def command_quote(number):
    try:
        the_file_name = 'quotes.txt'
        line_quote = linecache.getline(the_file_name, number)
        send_message(CHAN, line_quote)

    except IndexError:
        send_message(CHAN, "Quote IndexError: Cannot choose from an empty sequence. Add quotes.")
        print("-- ERROR: IndexError, Cannot choose from an empty sequence. Add quotes.")
        print(number)
        pass
    except KeyError:
        random_quote()
        pass


def random_quote():

    line_count = 0

    with open('quotes.txt') as file_open:
        for lines in file_open:
            if lines.strip():
                line_count += 1
    number = random.randint(0, line_count+1)

    if number % 2 == 0:
        random_quote()
    else:
        command_quote(number)


def command_run():
    send_message(CHAN, run)


def frankerz():
    send_message(CHAN, "FrankerZ")  # example without !<command>


# ------------- #
# ---- Mod ---- #
# ------------- #
def command_on():
    send_message(CHAN, "I am online and sending messages.")  # optional
    # send_message(CHAN, "Test on Whispering.")


def command_admin():
    send_message(CHAN, sender + " is a mod.")  # optional


def command_quote_add(quote_list):
    quotes = open('quotes.txt', 'a')
    quote = ' '.join(quote_list)
    quotes.write('"' + quote + '" ~ ' + BROADCASTER[0].upper() + BROADCASTER[1:20] + ", " + str(datetime.date.today().year))
    quotes.write("\r\n")
    quotes.close()
    send_message(CHAN, "Quote Added: " + quote)


def command_run_update(run_update):
    global run
    run = ' '.join(run_update)
    return run


def command_check(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    name = name[0].lower()
    check = c.execute("SELECT * FROM tableOut WHERE name LIKE ?", [str(name)])
    if str(name) in list(map(lambda x: x[0], check)):
        send_message(CHAN, name[0].upper() + name[1:50] + " is in the database.")
    else:
        send_message(CHAN, name[0].upper() + name[1:50] + " is not in the database.")
    conn.commit()
    conn.close()


def command_add(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    name = name[0].lower()
    c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [name])
    print((name[0].upper() + name[1:50] + " added."))
    conn.commit()
    conn.close()


# Viewers
def threading_timer():
    threading.Timer(UPDATE, threading_timer)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    global user_mods

    user_mods = list(map(lambda x: x[0], c.execute("SELECT * from tableOut WHERE mod = 1;")))
    conn.commit()
    conn.close()

    update_user_sf()

    send_message(CHAN, "Mods Updated.")
    return user_mods


# ViewersUpdate
def update_command():
    global UPDATE
    return_x(UPDATE-1)
    update_user_sf()
    send_message(CHAN, "Viewers Updated.")


def promote_mod(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    ''.join(name[0])
    check = c.execute("SELECT * FROM tableOut WHERE name LIKE ?", [name[0]])
    if name in list(map(lambda x: x[0], check)):
        try:
            send_message(CHAN, "/mod " + name[0])
            c.execute("UPDATE tableOut SET mod = 1 WHERE name = ?", [name[0]])
            send_message(CHAN, (name[0])[0].upper() + (name[0])[1:50] + " is now a mod.")
            print(name[0] + " is now a mod.")
        except sqlite3.OperationalError:
            send_message(CHAN, (name[0])[0].upper() + (name[0])[1:50] + " not found in database.")
            pass
    else:
        send_message(CHAN, (name[0])[0].upper() + (name[0])[1:50] + " not found in database.")
    conn.commit()
    conn.close()


def update_user_sf():
    global user_subs, user_fols
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if SUBS == 1:
        user_subs = list(map(lambda x: x[0], c.execute("SELECT name from tableOut WHERE sub = 1")))
    user_fols = list(map(lambda x: x[0], c.execute("SELECT name from tableOut WHERE fol = 1")))
    conn.commit()
    conn.close()

    return user_subs, user_fols


# - Play Commands - BETA - Volume Set in Dev
def command_play_pause():
    if MUSIC_ENABLED == 1:
        try:
            press_key(0xB3)
            release_key(0xB3)
        except NameError:
            send_message(CHAN, "NameError on !p")
            pass


def command_play_next():
    if MUSIC_ENABLED == 1:
        try:
            press_key(0xB0)
            release_key(0xB0)
        except NameError:
            send_message(CHAN, "NameError on !pn")
            pass


def command_play_pre():
    if MUSIC_ENABLED == 1:
        try:
            press_key(0xB1)
            release_key(0xB1)
        except NameError:
            send_message(CHAN, "NameError on !pp")
            pass


# --------------------- #
# ---- BROADCASTER ---- #
# --------------------- #
def command_off():
    send_message(CHAN, "Logging Off...")
    updates = subprocess.Popen(['python', 'update.py'])
    subprocess.Popen.terminate(updates)
    print("You need to close this window for the bot to fully turn off.")
    exit()


# ---------------- #
# ---- System ---- #
# ---------------- #


# ---- Background Systems ---- #
def command_start_all():

    if MEDIA_ENABLED == 1:
        title()
        print(TITLE)
        print("-- SYSTEM: Broadcast Enabled.")

    if BROADCAST_ENABLED == 1:
        printout()
        print(BROADCAST)
        print("-- SYSTEM: Broadcast Enabled.")

    if CURRENCY_ENABLED == 1:
        currency_reward_timer()
        print("-- SYSTEM: Currency Enabled.")

    if MUSIC_ENABLED == 1:
        print("-- SYSTEM: Music Enabled.")

    if MUSIC_ENABLED and BROADCAST_ENABLED and CURRENCY_ENABLED and MEDIA_ENABLED == 0:
        print("-- SYSTEM: No Extra Features Loaded.")


def title():
    threading.Timer(TITLE_SHOWN, title)
    send_message(CHAN, TITLE)


def printout():
    threading.Timer(BROADCAST_SHOWN, BROADCAST)
    send_message(CHAN, SOCIAL_MEDIA)


def command_timeout_auto_1(name):

    if name not in user_mods:
        send_message(CHAN, '/timeout ' + name + ' 1')


# ---- SQL Based ---- #
def command_timeout_auto(name):
    if name not in user_mods:
        send_message(CHAN, '/timeout ' + name + ' ' + str(TIMEOUT_TIME))
        # for users in user_mods:
        # whisper(users, name + ' has been timed out for 45 second(s).')  # optional
        print("-- OFFENSE: " + name + " has been timed out for 30 second(s).")
    else:
        print("-- SYSTEM: " + name + " cant not be timed out.")  # optional


def conntest():
    try:
        conn = sqlite3.connect(DATABASE)
        send_message(CHAN, "Connection Successful.")
        print("-- DATABASE: Connection Successful.")
        conn.commit()
        conn.close()
    finally:
        print("")


# --------------- #
# Currency System #
# --------------- #
def currency_reward_timer():
    threading.Timer(UPDATE_CURRENCY, currency_reward_timer)


def command_stats():
    name = sender
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    name_check = list(map(lambda x: x[0], c.execute("SELECT * FROM tableOut WHERE name LIKE ?", [name])))
    if name in name_check:
        for stats in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name]):
            for offenses in c.execute("SELECT timeout FROM tableOut WHERE name LIKE ?", [name]):
                if CURRENCY_ENABLED == 0:
                    send_message(CHAN, name + ", " + str(offenses[0]) + " offenses.")
                if CURRENCY_ENABLED == 1:
                    send_message(CHAN, name + ", you have $" + str(stats[0]) + " and " + str(offenses[0]) + " offenses")
                break
            break
    else:
        send_message(CHAN, "@" + name + ", you are not found in the database.")
    conn.commit()
    conn.close()


# SQL Database Code
def sql_timeout(name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Insert a row of data
    c.execute("INSERT OR IGNORE INTO tableOut (name,timeout) VALUES (?,0);", [name])
    #  Update timeout Warnings
    c.execute("UPDATE tableOut SET timeout = timeout + 1 WHERE name = ?;", [name])
    for times in c.execute("SELECT timeout FROM tableOut WHERE timeout <= ? and name LIKE ?", [5, name]):
        out = int(times[0])
        print("-- OFFENSE: " + name + " = " + str(out) + "/3")
        send_message(CHAN, sender + ", warning. " + str(out) + "/3")
        if out >= TIMEOUT_LIMIT:
            c.execute("UPDATE tableOut SET timeout = timeout - ? WHERE name = ?;", [TIMEOUT_LIMIT, name])
            command_timeout_auto(name)
            send_message(CHAN, "Offences set to 0 for " + name + ".")
            print("-- DATABASE: " + name + " reset to 0 offenses.")
            if CURRENCY_ENABLED == 1:
                c.execute("UPDATE tableOut SET currency = currency - ? WHERE name = ?;", [CURRENCY_MINUS, name])
        break
    else:
        out = 0  # not found
        name_out = ''  # nothing
        if name_out == '':
            out += 0
    conn.commit()
    conn.close()


# --------------------------------------------- End Command Functions ---------------------------------------------- #

# Leave all this alone.

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""
BOT_ENABLED = 1
temp_mod = []


def update_viewers_mods():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    return_x(UPDATE-1)
    mod = "SELECT * from tableOut WHERE mod = 1;"
    mod_save = list(map(lambda x: x[0], c.execute(mod)))
    return mod_save


def send_mod():
    send_message(CHAN, update_viewers_mods())


def connect_no_mod():

    global connect_bot, temp_mod, BOT_ENABLED, NICK, user_mods, start

    user_mods = mod_update()
    viewers = viewer_update()
    update_user_sf()

    if NICK in user_mods or BOT_ENABLED == 1:
        print(chr(27) + "[2J")
        return_x(UPDATE-1)
        print("")
        print("-- BOT: Connected to " + USER + ". Online and ready. Version 1.4.5b")
        print("")
        print("Current Mods:")
        for mod in user_mods:
            print(mod)
        print("")

        send_message(CHAN, "/TWITCHCLIENT 3")

        command_start_all()
        update_viewers_mods()

        start = datetime.datetime.now()
        BOT_ENABLED = 1
        return BOT_ENABLED

    elif NICK in viewers:
        if temp_mod != user_mods:
            print(user_mods)
        else:
            temp_mod = user_mods
        t = threading.Timer(1.0, connect_no_mod)
        if connect_bot == 150:
            print("This connection does take time.")
        if connect_bot >= 300:
            print("Something is wrong. Restart is best bet. ")
            print("Check the vars.json files to make sure everything is correct.")
            sleep(4)
            exit()
        connect_bot += 1
        print("-- BOT: [" + str(connect_bot) + "] " + "Waiting to find as Mod...")
        t.start()

    else:
        if temp_mod != user_mods:
            print(user_mods)
            temp_mod = user_mods
        else:
            temp_mod = user_mods
        t = threading.Timer(1.0, connect_no_mod)
        connect_bot += 1
        print("-- BOT: [" + str(connect_bot) + "] " + "Trying to connect...")
        t.start()


def startup():

    print("-- BOT: Connecting to " + USER + "...")

    global start
    global user_mods
    global NICK
    update_viewers_mods()
    if NICK in user_mods:
        connect_no_mod()
    else:
        update_viewers_mods()
        print("-- WARNING: Not found in user mods. Waiting...")
        connect_no_mod()


startup()


while True:
        try:

            data = data+con.recv(1024).decode('UTF-8')
            data_split = re.split(r"[~\r\n]+", data)
            data = data_split.pop()

            for line in data_split:
                line = str.rstrip(line)
                line = str.split(line)
                if len(line) >= 1:
                    try:

                        if line[0] == 'PING':
                            send_pong(line[1])

                        if line[1] == 'PRIVMSG':
                            sender = get_sender(line[0])
                            message = get_message(line)
                            parse_message(message)

                            if sender in user_mods:
                                print("[MOD]" + sender + ": " + message)
                            elif SUBS == 0 and (sender in user_fols) and (sender not in user_mods):
                                print("[FOL]" + sender + ": " + message)
                            elif SUBS == 1 and sender in user_subs and sender not in user_mods:
                                print("[SUB]" + sender + ": " + message)
                            else:
                                print(sender + ": " + message)

                    except IndexError:
                            # Catches "~" in chat to not error
                            pass

        except socket.error or socket.timeout:
            print("-- WARNING[IRC]: Socket died")

        except socket.timeout:
            print("-- WARNING[IRC]: Socket timeout")

        except socket.timeout or socket.error:
            string_start = input("-- SYSTEM: Attempt a Restart? Y/N")
            yes = {'yes', 'YES', 'y', 'Y', '+'}
            no = {'no', 'NO', 'n', 'N', '-'}
            if string_start in yes:
                print("-- BOT: Attempting Restart...")
                startup()
            elif string_start in no:
                print("-- SYSTEM: Exiting...")
                exit()
