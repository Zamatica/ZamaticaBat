# !/usr/bin/env python3
import json
import sqlite3
import urllib.request
import urllib.error
import os
from sys import exit
from time import sleep

import config.variable as variable

USERS = variable.USERS
UPDATE = variable.UPDATE


URL = "https://tmi.twitch.tv/group/user/" + variable.USER + "/chatters"
x = 0
global_subs, global_followers = [], []

user_mods, user_subs, user_followers, editors = {}, {}, {}, {}


def update_timer():
    global UPDATE, x
    while os.path.isfile("bin/systems/connection.txt"):
        if x >= UPDATE:
            update()
            return_x(0)
        elif x < UPDATE:
            x += 1
            return_x(x)
            sleep(1)
    if os.path.isfile("bin/systems/connection.txt") is False:
        print("Updates Exiting...")
        exit()


def return_x(save):
    global x
    x = save
    return x


def update_mod():
    return_x(UPDATE)


def update():
    global user_mods, user_followers, user_subs
    viewers_count = 0
    mod_count = 0
    viewers = get_viewers()
    mods = get_mods()
    if variable.FOLLOWER_ENABLED == 1:
        followers = get_followers()
        follower_count = 0
        for follower in followers:
            follower_count += 1
        user_followers = followers
        print("-- CHANNEL: Currently " + str(follower_count) + " followers.")
    if variable.SUB_ENABLED == 1:
        sub_count = 0
        subs = get_subs()
        for sub in subs:
            sub_count += 1
        print("-- CHANNEL: Currently " + str(sub_count) + " subs watching.")
        user_subs = subs
    for viewer in viewers:
        viewers_count += 1
    for mod in mods:
        mod_count += 1
    follower_sub_update()
    print("")
    print("-- IRC: There are currently " + str(viewers_count) + " people watching and " + str(mod_count) + " moderators modding.\n        Total: " + str(mod_count + viewers_count) + "\n")
    user_mods = mods
    return user_mods, user_followers, user_subs


def get_viewers():
    try:
        viewer_data = urllib.request.urlopen(URL)
        viewer_list = json.loads(viewer_data.read().decode(viewer_data.info().get_param('charset') or 'utf-8'))
        database_save(viewer_list)
        return viewer_list["chatters"]["viewers"]
    except urllib.error.HTTPError:
        print("-- WARNING: 502 Bad Gateway.")


def get_mods():
    try:
        mod_data = urllib.request.urlopen(URL)
        mod_list = json.loads(mod_data.read().decode(mod_data.info().get_param('charset') or 'utf-8'))
        database_save(mod_list, 3)
        return mod_list["chatters"]["moderators"]
    except urllib.error.HTTPError:
        print("-- WARNING: 502 Bad Gateway.")


def get_followers():
    try:
        url_followers = urllib.request.urlopen("https://api.twitch.tv/kraken/channels/" + variable.USER + "/follows").read().decode()
        json_followers = json.loads(url_followers)
        follower_list = []
        follower_count = 0
        while follower_count < len(json_followers['follows']):
            follower = json_followers['follows'][follower_count]['user']['name']
            follower_list.append(follower)
            follower_count += 1
        database_save(follower_list, 1)
        return follower_list
    except urllib.error.HTTPError:
        print("-- WARNING: 502 Bad Gateway")


def get_subs():
    try:
        url_sub = urllib.request.urlopen("https://api.twitch.tv/kraken/channels/" + variable.USER + "/subscriptions?oauth_token=" + variable.SUB_OAUTH)
        json_sub = json.loads(url_sub)
        sub_list = []
        sub_count = 0
        while sub_count < len(json_sub):
            sub = json_sub['subscriptions'][sub_count]['user']['name']
            sub_list.append(sub)
            sub_count += 1
        database_save(sub_list, 2)
        return sub_list
    except urllib.error.HTTPError:
        print("")
        print("-- WARNING: HTTP Error.")
        print("-- WARNING: No Sub Program or Broken Sub oAuth")
        input("-- WARNING: Restart or Set Subs to 0 and Restart.")


def follower_sub_update():
    global global_subs, global_followers
    conn = sqlite3.connect(USERS)
    c = conn.cursor()
    if variable.SUB_ENABLED == 1:
        global_subs = list(map(lambda selected: selected[0], c.execute("SELECT name from users WHERE sub = 1")))
    global_followers = list(map(lambda selected: selected[0], c.execute("SELECT name from users WHERE follower = 1")))
    conn.commit()
    conn.close()
    return global_subs, global_followers


def database_save(user_list, save_id=0):
    conn = sqlite3.connect(USERS)
    c = conn.cursor()
    if save_id == 0:
        for user in user_list:
            c.execute("INSERT OR IGNORE INTO users (name) VALUES (?);", [user])
    elif save_id == 1 and variable.FOLLOWER_ENABLED == 1:
        for follower in user_list:
            c.execute("INSERT OR IGNORE INTO users (name) VALUES (?);", [follower])
            c.execute("UPDATE users set follower = 1 WHERE name like ?;", [follower])
    elif save_id == 2 and variable.SUB_ENABLED == 1:
        for sub in user_list:
            c.execute("INSERT OR IGNORE INTO users (name) VALUES (?);", [sub])
            c.execute("UPDATE users set sub = 1 WHERE name like ?;", [sub])
    elif save_id == 3:
        for mod in user_list:
            c.execute("INSERT OR IGNORE INTO users (name) VALUES (?);", [mod])
            c.execute("UPDATE users set mod = 1 WHERE name like ?;", [mod])
    conn.commit()
    conn.close()
