# !/usr/bin/env python3
import sqlite3, threading
from sys import path
import connections as con
import vars as variable

USERS = 'users/users.db'

send_message = con.send_message


def command_start_all():

    if variable.MEDIA_ENABLED == 1:
        social_media_func()
        print(variable.SOCIAL_MEDIA)
        print("-- SYSTEM: Social Media Enabled.")

    if variable.TITLE_ENABLED == 1:
        title()
        print(variable.TITLE)
        print("-- SYSTEM: Title Enabled.")

    if variable.BROADCAST_ENABLED == 1:
        printout()
        print(variable.BROADCAST)
        print("-- SYSTEM: Broadcast Enabled.")

    if variable.CURRENCY_ENABLED == 1:
        currency_reward_timer()
        print("-- SYSTEM: Currency Enabled.")

    if variable.MUSIC_ENABLED == 1:
        print("-- SYSTEM: Music Enabled.")

    if (variable.MUSIC_ENABLED + variable.BROADCAST_ENABLED + variable.CURRENCY_ENABLED + variable.MEDIA_ENABLED + variable.TITLE_ENABLED) == 0:
        print("-- SYSTEM: No Extra Features Loaded.")


def title():
    threading.Timer(variable.TITLE_SHOWN, title)
    send_message(variable.TITLE)


def social_media_func():
    threading.Timer(variable.MEDIA_SHOWN, social_media_func)
    send_message(variable.SOCIAL_MEDIA)


def printout():
    threading.Timer(variable.BROADCAST_SHOWN, printout)
    send_message(variable.BROADCAST)


def command_timeout_auto_1(name):
    send_message('/timeout ' + name + ' 1')


def command_timeout_auto(name):
        send_message('/timeout ' + name + ' ' + str(variable.TIMEOUT_TIME))
        # for users in user_mods:
        # whisper(users, name + ' has been timed out for 45 second(s).')  # optional
        print("-- OFFENSE: " + name + " has been timed out for 30 second(s).")


def conntest():
    try:
        conn = sqlite3.connect(USERS)
        send_message("Connection Successful.")
        print("-- USERS: Connection Successful.")
        conn.commit()
        conn.close()
    finally:
        print("")


# --------------- #
# Currency System #
# --------------- #
def currency_reward_timer():
    threading.Timer(variable.UPDATE_CURRENCY, currency_reward_timer)


def sql_timeout(name):
    conn = sqlite3.connect(USERS)
    c = conn.cursor()
    # Insert a row of data
    c.execute("INSERT OR IGNORE INTO tableOut (name,timeout) VALUES (?,0);", [name])
    #  Update timeout Warnings
    c.execute("UPDATE tableOut SET timeout = timeout + 1 WHERE name = ?;", [name])
    for times in c.execute("SELECT timeout FROM tableOut WHERE timeout <= ? and name LIKE ?", [5, name]):
        out = int(times[0])
        print("-- OFFENSE: " + name + " = " + str(out) + "/3")
        send_message(name + ", warning. " + str(out) + "/3")
        if out >= variable.TIMEOUT_LIMIT:
            c.execute("UPDATE tableOut SET timeout = timeout - ? WHERE name = ?;", [variable.TIMEOUT_LIMIT, name])
            command_timeout_auto(name)
            send_message("Offences set to 0 for " + name + ".")
            print("-- USERS: " + name + " reset to 0 offenses.")
            if variable.CURRENCY_ENABLED == 1:
                c.execute("UPDATE tableOut SET currency = currency - ? WHERE name = ?;", [variable.CURRENCY_MINUS, name])
        break
    else:
        out = 0  # not found
        name_out = ''  # nothing
        if name_out == '':
            out += 0
    conn.commit()
    conn.close()
