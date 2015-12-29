__author__ = 'Zamatica'

import sqlite3
import urllib.request
import urllib.error
import json
from time import sleep
from sys import exit

DATABASE = 'users.db'

with open("vars.json") as file:
    VARS = json.load(file)

USER = VARS["connection"]["CHAN"][1:100]

URL = "https://tmi.twitch.tv/group/user/" + USER + "/chatters"

FOL = int(VARS["variables"]["FOL"])
SUBS = int(VARS["variables"]["SUBS"])
SUB_OAUTH = VARS["variables"]["SUB_OAUTH"]

UPDATE = float(VARS["variables"]["UPDATE"])

CURRENCY_ENABLED = int(VARS["variables"]["CURRENCY_ENABLED"])
CURRENCY_VALUE = int(VARS["variables"]["CURRENCY_VALUE"])  # Set value of currency, default 15

x = 0


def update_timer():
    global UPDATE, x
    while True:
        x += 1
        if x == UPDATE:
            update_start()
            return_x(0)
        elif x < UPDATE:
            return_x(x)
            sleep(1)


def return_x(save):
    global x
    x = save
    return x


# Updating Viewer List
def update_all(data_loaded):
    num = 0
    num_mods = 0
    users = data_loaded["chatters"]["viewers"]
    mods = data_loaded["chatters"]["moderators"]
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for name in users:
        c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [name])
        c.execute("UPDATE tableOut SET mod = 0 WHERE name = ?;", [name])
        num += 1
    for name_mods in mods:
        c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [name_mods])
        c.execute("UPDATE tableOut SET mod = 1 WHERE name = ?;", [name_mods])
        num_mods += 1
    print("-- IRC: There are " + str(len(users)) + " viewing and " + str(len(mods)) + " moderators currently watching.")
    conn.commit()
    conn.close()
    if SUBS == 1:
        sub_update()
    elif SUBS != 1 and FOL == 1:
        fol_update()
    elif CURRENCY_ENABLED == 1:
        currency_reward(data_loaded)


def update_start():
    try:
        response = urllib.request.urlopen(URL)
        data_save = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        return update_all(data_save)

    except urllib.error.HTTPError:
        print("-- WARNING: 502 Bad Gateway. Updating Every 2 minutes.")
        pass
        global UPDATE
        UPDATE = 120
        return UPDATE, return_x(0)


def mod_update():
    try:
        mod_data = urllib.request.urlopen(URL)
        mod_list = json.loads(mod_data.read().decode(mod_data.info().get_param('charset') or 'utf-8'))
        return mod_list["chatters"]["moderators"]
    except urllib.error.HTTPError:
        print("-- WARNING: 502 Bad Gateway.")


def viewer_update():
    try:
        viewer_data = urllib.request.urlopen(URL)
        viewer_list = json.loads(viewer_data.read().decode(viewer_data.info().get_param('charset') or 'utf-8'))
        return viewer_list["chatters"]["viewers"]
    except urllib.error.HTTPError:
        print("-- WARNING: 502 Bad Gateway.")


# --------------------------------------------------------------------------------------------------------------------------------------------- #

def currency_reward(data_loaded):
    users = data_loaded["chatters"]["viewers"]
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for name in users:
        c.execute("UPDATE tableOut SET currency = currency + ? WHERE name = ?;", [CURRENCY_VALUE, name])
    print("-- DATABASE: Currency list for viewer list updated.")
    conn.commit()
    conn.close()

# --------------------------------------------------------------------------------------------------------------------------------------------- #


# Subscribers
def sub_update():
    try:
        res_sub = urllib.request.urlopen("https://api.twitch.tv/kraken/channels/" + USER + "/subscriptions?oauth_token=" + SUB_OAUTH)
        data_subs = json.loads(res_sub)
        ws = []
        s = 0
        while s < len(data_subs['subscriptions']):
            user_sub = data_subs['subscriptions'][s]['user']['name']
            ws.append(user_sub)
            s += 1
        sub_database(ws)
    except urllib.error.HTTPError:
        print("No Sub Program. Set subs to 0.")
        exit()


def sub_database(subs):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for sub in subs:
        c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [sub])
        c.execute("UPDATE tableOut set sub = 1 WHERE name like ?", [sub])
    conn.commit()
    conn.close()


# Followers
def fol_update():
    res_fol = urllib.request.urlopen("https://api.twitch.tv/kraken/channels/" + USER + "/follows").read().decode()
    data_fol = json.loads(res_fol)
    z = 0
    wt = []
    while z < len(data_fol['follows']):
        fol_user = data_fol['follows'][z]['user']['name']
        wt.append(fol_user)
        z += 1
    fol_database(wt)


def fol_database(fols):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for fol in fols:
        c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [fol])
        c.execute("UPDATE tableOut set fol = 1 WHERE name like ?", [fol])
    conn.commit()
    conn.close()
