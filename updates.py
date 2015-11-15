__author__ = 'Zamatica'

import sqlite3
import urllib.request
import urllib.error
import json

DATABASE = 'users.db'

with open("vars.json") as file:
    VARS = json.load(file)

USER = VARS["connection"]["CHAN"][1:100]

URL = "https://tmi.twitch.tv/group/user/" + USER + "/chatters"

SUBS = int(VARS["variables"]["SUBS"])
SUB_OAUTH = VARS["variables"]["SUB_OAUTH"]

CURRENCY_VALUE = int(VARS["variables"]["CURRENCY_VALUE"])  # Set value of currency, default 15


def update_viewers():
    global user_reg
    response = urllib.request.urlopen(URL)
    data_save = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    user_reg = data_save["chatters"]["viewers"]
    if SUBS == 1:
        sub_update()
    fol_update()
    return user_reg


# Moderators
def update_viewers_mods():
    response = urllib.request.urlopen(URL)
    data_save_mod = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    user_mods = data_save_mod["chatters"]["moderators"]
    return user_mods


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
        num += 1
    for name_mods in mods:
        c.execute("INSERT OR IGNORE INTO tableOut (name) VALUES (?);", [name_mods])
        num_mods += 1
    currency_reward(viewers())
    print("-- IRC: Viewer list updated. There are " + str(num) + " viewing. And " + str(num_mods) + " modding things.")
    conn.commit()
    conn.close()


def viewers():
    response = urllib.request.urlopen(URL)
    data_save = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return data_save


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
        while s < 100000000:
            try:
                user_sub = data_subs['follows'][s]['user']['name']
                ws.append(user_sub)
                s += 1
            except IndexError:
                break
        sub_database(ws)
    except urllib.error.HTTPError:
        print("No Sub Program. Set subs to 0.")


def sub_database(subs):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for sub in subs:
        c.execute("UPDATE tableOut set sub = 1 WHERE name like ?", [sub])
    conn.commit()
    conn.close()


# Followers
def fol_update():
    res_fol = urllib.request.urlopen("https://api.twitch.tv/kraken/channels/" + USER + "/follows").read().decode()
    data_fol = json.loads(res_fol)
    wt = []
    t = 0
    while t < 100000000:
        try:
            fol_user = data_fol['follows'][t]['user']['name']
            wt.append(fol_user)
            t += 1
        except IndexError:
            break
    fol_database(wt)


def fol_database(fols):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    for fol in fols:
        c.execute("UPDATE tableOut set fol = 1 WHERE name like ?", [fol])
    conn.commit()
    conn.close()
