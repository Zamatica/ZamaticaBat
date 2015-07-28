__author__ = 'Force3'

# !/usr/bin/env python3

import re
import socket
import sys
import datetime
import sqlite3
import threading
import json
import urllib.request
import random
import linecache

# --------------------------------------------- Start Settings ---------------------------------------------------- #

with open("vars.json") as file:
    VARS = json.load(file)


HOST = VARS["connection"]["HOST"]            # Host
PORT = VARS["connection"]["PORT"]            # Port
CHAN = VARS["connection"]["CHAN"]            # # + Your Twitch Username
NICK = VARS["connection"]["NICK"]            # Your Bot's Twitch username
PASS = VARS["connection"]["PASS"]            # http://www.twitchapps.com/tmi/ -- Talk to Zamatica about this.

PORT = int(PORT)

# User Variables

# Variables -- 1 = On/0 = Off

start = datetime.datetime.now()


URL = VARS["variables"]["CHATTERS"]


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

# VARIABLE = {}  <-- {'word', 'word2', 'word3'} can have more than 3

BANNED_WORDS = VARS["variables"]["BANNED_WORDS"]   # ... add what ever you like, no spaces, ALL LOWERCASE


BROADCASTER = VARS["variables"]["BROADCASTER"]  # YOU, Editors, and anyone you trust with this, ALL LOWERCASE

# Currency - BETA
CURRENCY_ENABLED = int(VARS["variables"]["CURRENCY_ENABLED"])  # Reward for spending time, default 0

CURRENCY_MINUS = int(VARS["variables"]["CURRENCY_MINUS"])  # Punishment for offenses, default 20. Want to disable? make 0

UPDATE_CURRENCY = int(VARS["variables"]["UPDATE_CURRENCY"])  # Time for currency to be added, in seconds, default 3600 (1 hour)

CURRENCY_VALUE = int(VARS["variables"]["CURRENCY_VALUE"])  # Set value of currency, default 15

# End User Variables

# System Variables
DATABASE = 'users.db'

connect_bot = 0

run = 'Nothing right now.'

user_reg = {}
user_mods = {}


def update_viewers_mods():

    threading.Timer(15.0, update_viewers_mods)

    response = urllib.request.urlopen(URL)

    data_save_mod = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    global user_mods

    user_mods = data_save_mod["chatters"]["moderators"]

    return user_mods


def update_viewers():

    threading.Timer(UPDATE, update_viewers)

    response = urllib.request.urlopen(URL)

    data_save = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    global user_reg

    user_reg = data_save["chatters"]["viewers"]

    return user_reg


# --------------------------------------------- End Settings ------------------------------------------------------- #


# --------------------------------------------- Start Functions ---------------------------------------------------- #

def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


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

BOT_ENABLED = 0


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
                    command_timeout_auto_1(sender)
                    send_message(CHAN, "We can hear you just fine " + sender)

            options = {}
            options_3 = {}
            options_mod = {}
            options_mod_1 = {}
            options_mod_4 = {}
            options_broad = {}

            if sender is not 'ded':

                options = {

                    '!test': command_test,
                    '!asdf': command_asdf,
                    '!uptime': command_uptime,
                    '!time': command_time,
                    '!help': command_help,
                    '!stats': command_stats,
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
                    '!off': command_nowhere
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
                    '!update': viewers_update_command,

                }

                options_mod_1 = {

                    '!quoteadd': command_quote_add,
                    '!runset': command_run_update,

                }

            if sender in BROADCASTER:

                options_broad = {

                    # Commands only given to BroadCaster(s) from BROADCASTER VARIABLE
                    '!off': command_off,
                    '!broad': command_start_all,
                    '!conn': conntest,

                }

            # Ignore Me
            if msg[0] in options:
                options[msg[0]]()

            elif msg[0] in options_mod:
                options_mod[msg[0]]()

            elif msg[0] in options_mod_1:
                try:
                    options_mod_1[msg[0]](msg[1:50])
                except KeyError:
                    # Key is not present
                    send_message(CHAN, 'One parameter is required.')
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

            elif msg[0] in options_broad:
                options_broad[msg[0]]()

# --------------------------------------------- End Helper Functions ----------------------------------------------- #

# --------------------------------------------- Start Command Functions -------------------------------------------- #


# ---- User ---- #

def command_nowhere():
    if sender not in user_mods:
        print(sender + " tried to use a banned command.")

    return sql_timeout(sender)


def command_nowhere_auto(name):

    print(name + " has made on offense.")

    return sql_timeout(name)


def command_null():
    a = 0
    a += 1


def command_help():
    if sender in user_mods:
        send_message(CHAN, 'There is !help, !coin, !ping, !asdf, !uptime, !time, !stats, !runset, !test, !on, !admin, !runtime, !ping, !addquote, and !update')
    else:
        send_message(CHAN, 'There is !help, !ping, !asdf, !uptime, !time, !stats, !run, !coin, and !test')


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


def command_asdf():
    send_message(CHAN, 'Master Blasters!')


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
            for timeout in c.execute("SELECT timeout FROM tableOut WHERE name LIKE ?", [name]):
                timeouts = timeout[0]
                if timeouts > 0:
                    for stats in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name]):
                        if stats[0] >= (CURRENCY_VALUE*4)*int(quantity[0]):
                            c.execute("UPDATE tableOut SET currency = currency - ? WHERE name = ?;", [CURRENCY_VALUE*4*int(quantity[0]), name])
                            c.execute("UPDATE tableOut SET timeout = timeout - ? WHERE name = ?;", [quantity[0], name])
                            conn.commit()
                            for stats_new in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name]):
                                for timeout_new in c.execute("SELECT timeout FROM tableOut WHERE name LIKE ?", [name]):
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

    conn.close()


def command_coin(cmd, amount, name):

    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    name_0 = name
    amount_0 = amount

    if CURRENCY_ENABLED == 1:
        if sender in user_mods:
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
            for value in c.execute("SELECT currency FROM tableOut WHERE name like ?", name_0):
                send_message(CHAN, name_0 + ", you have $" + value + ".")

    else:
        send_message(CHAN, "Currency Disabled.")

    conn.close()


def command_quote(number):
    try:

        the_file_name = 'quotes.txt'
        line_quote = linecache.getline(the_file_name, number)

        send_message(CHAN, line_quote)

    except IndexError:
        send_message(CHAN, "Error: Cannot choose from an empty sequence.")
        print("-- ERROR: IndexError, Cannot choose from an empty sequence.")
        print(number)


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
    send_message(CHAN, "ZamaticaBat is online and running properly.")  # optional


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


# --------------------- #
# ---- BROADCASTER ---- #
# --------------------- #
def command_off():
    send_message(CHAN, "Logging Off...")
    sys.exit()


# ---------------- #
# ---- System ---- #
# ---------------- #

# ---- Background Systems ---- #
def command_start_all():
    title()
    printout()
    if CURRENCY_ENABLED == 1:
        currency_reward_timer()


def title():
    threading.Timer(TITLE_SHOWN, title).start()
    send_message(CHAN, TITLE)


def printout():
    threading.Timer(BROADCAST_SHOWN, BROADCAST).start()
    send_message(CHAN, SOCIAL_MEDIA)


def command_timeout_auto_1(name):

    if name not in user_mods:
        send_message(CHAN, '/timeout ' + name + ' 1')


# ---- SQL Based ---- #
def command_timeout_auto(name):

    if name not in user_mods:
        send_message(CHAN, '/timeout ' + name + ' ' + str(TIMEOUT_TIME))
        send_message(CHAN, name + ' has been timed out for 45 second(s).')  # optional
        print("-- OFFENSE: " + name + " has been timed out for 30 second(s).")
    else:
        send_message(CHAN, name + " cant not be timed out.")  # optional


def conntest():
    try:
        conn = sqlite3.connect(DATABASE)
        send_message(CHAN, "Connection Successful.")
        print("-- DATABASE: Connection Successful.")
        conn.close()
    finally:
        print("")


# Viewers
def viewers_update_command():
    # Saves data_save
    update = viewers()
    # passes data_save to reward_viewers
    reward_viewers(update)


def viewers():
    response = urllib.request.urlopen(URL)
    data_save = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return data_save


def reward_viewers(data_loaded):

    num = 0
    num_mods = 0

    users = data_loaded["chatters"]["viewers"]
    mods = data_loaded["chatters"]["moderators"]

    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    for name in users:
        c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [name])
        num += 1
    for name_mods in mods:
        c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [name_mods])
        num_mods += 1

    print("-- DATABASE: Viewer list updated. There are " + str(num) + " viewing. And " + str(num_mods) + " modding things.")

    conn.commit()

    conn.close()


def viewer_update():
    threading.Timer(UPDATE, viewer_update)
    # Saves data_save
    update = viewers()
    # passes data_save to reward_viewers
    reward_viewers(update)


# Currency - BETA
def currency_reward_timer():

    threading.Timer(UPDATE_CURRENCY, currency_reward_timer)

    update = viewers()

    reward_viewers(update)


def command_stats():

    viewer_update()

    name = sender

    conn = sqlite3.connect(DATABASE)
    print("-- DATABASE: Connection Opened.")

    c = conn.cursor()

    for stats in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [name]):
        for offenses in c.execute("SELECT timeout FROM tableOut WHERE name LIKE ?", [name]):

            if CURRENCY_ENABLED == 0:
                send_message(CHAN, name + ", " + str(offenses[0]) + " offenses.")
            if CURRENCY_ENABLED == 1:
                send_message(CHAN, name + ", you have $" + str(stats[0]) + " and " + str(offenses[0]) + " offenses")

            print("-- USERS: " + name + " has requested stats.")

            break
        break

    conn.close()
    print("-- DATABASE: Connection Closed.")


# SQL for Currency
def currency_reward(data_loaded):

    users = data_loaded["chatters"]["viewers"]

    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    for name in users:
        c.execute("UPDATE tableOut SET currency = currency + ? WHERE name = ?;", [CURRENCY_VALUE, name])

    print("-- DATABASE: Currency list for viewer list updated.")

    conn.commit()

    conn.close()


# SQL Database Code
def sql_timeout(name):

    # SQL
    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()
    print("-- DATABASE: Connected to Database.")

    # Insert a row of data
    c.execute("INSERT OR IGNORE INTO tableOut (name,timeout) VALUES (?,0);", [name])
    #  Update timeout Warnings
    c.execute("UPDATE tableOut SET timeout = timeout + 1 WHERE name = ?;", [name])

    for times in c.execute("SELECT timeout FROM tableOut WHERE timeout <= ? and name LIKE ?", [5, name]):
        out = int(times[0])

        print("-- OFFENSE: " + name + " = " + str(out) + "/3")

        send_message(CHAN, sender + ", tried to use a banned command. " + str(out) + "/3")

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
        nameout = ''  # nothing
        if nameout == '':
            out += 0
    # Saves Data
    print("-- DATABASE: Database Saved and Closed.")
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


def connect_no_mod():

    global start
    global user_mods
    global NICK

    update_viewers_mods()

    if NICK in user_mods:

        update_viewers_mods()
        update_viewers()

        send_message(CHAN, "Connected to " + CHAN[1:100] + ". Online and ready.")

        print("-- BOT: Connected to " + CHAN[1:100] + ". Online and ready. Version 1.3")
        if MEDIA_SHOWN == 1:
            printout()

            title()

        viewers()
        update_viewers_mods()
        update_viewers()

        start = datetime.datetime.now()

        global BOT_ENABLED

        BOT_ENABLED = 1

        return BOT_ENABLED

    else:

        global connect_bot

        t = threading.Timer(5.0, connect_no_mod)

        connect_bot += 1

        print("[" + str(connect_bot) + "] " + "Trying to connect...")

        t.start()


def startup():
    print("Connecting to " + CHAN[1:10] + "...")

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
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message)

                    print(sender + ": " + message)

    except socket.error:
        print("-- WARNING: Socket died")
        string_start = input("-- SYSTEM: Restart? Y/N")
        yes = {'yes', 'YES', 'y', 'Y'}
        no = {'no', 'NO', 'n', 'N'}
        if string_start in yes:
            print("-- BOT: Restarting...")
            startup()
        elif string_start in no:
            print("-- SYSTEM: Exiting...")
            sys.exit()

    except socket.timeout:
        print("-- WARNING: Socket timeout")
