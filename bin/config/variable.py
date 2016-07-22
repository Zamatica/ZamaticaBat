# !/usr/bin/env python3
import json, datetime

with open("bin/config/vars.json") as file:
    VARS = json.load(file)

HOST = VARS["connection"]["HOST"]                  # Host
PORT = VARS["connection"]["PORT"]                  # Port

CHAN = VARS["connection"]["CHAN"]                  # # + Your Twitch Username
NICK = VARS["connection"]["NICK"]                  # Your Bot's Twitch username
PASS = VARS["connection"]["PASS"]                  # http://www.twitchapps.com/tmi/ -- Google This.

CHAN_WHISPER = VARS["connection"]["CHAN_WHISPER"]  # Channel for Whisper
HOST_WHISPER = VARS["connection"]["HOST_WHISPER"]  # Whisper Host

PORT = int(PORT)

#
start = datetime.datetime.now()
USER = VARS["connection"]["CHAN"][1:100]
BROADCASTER = VARS["variables"]["BROADCASTER"]
EDITORS = VARS["variables"]["EDITORS"]
#
TIMEZONE = VARS["variables"]["TIMEZONE"]
#
MEDIA_ENABLED = int(VARS["variables"]["MEDIA_ENABLED"])
MEDIA_SHOWN = float(VARS["variables"]["MEDIA_SHOWN"])
SOCIAL_MEDIA = VARS["variables"]["SOCIAL_MEDIA"]
MUSIC_ENABLED = int(VARS["variables"]["MUSIC_ENABLED"])
#
TITLE_ENABLED = int(VARS["variables"]["TITLE_ENABLED"])
TITLE = VARS["variables"]["TITLE"]
TITLE_SHOWN = float(VARS["variables"]["TITLE_SHOWN"])
#
BROADCAST_ENABLED = int(VARS["variables"]["BROADCAST_ENABLED"])
BROADCAST_SHOWN = float(VARS["variables"]["BROADCAST_SHOWN"])
BROADCAST = VARS["variables"]["BROADCAST"]
# Mod
TIMEOUT_TIME = int(VARS["variables"]["TIMEOUT_TIME"])
TIMEOUT_LIMIT = int(VARS["variables"]["TIMEOUT_LIMIT"])
BANNED_WORDS = VARS["variables"]["BANNED_WORDS"]
# Update Time on Viewers
UPDATE = float(VARS["variables"]["UPDATE"])
# Cases
FOLLOWER_ENABLED = int(VARS["variables"]["FOLLOWER_ENABLED"])
SUB_ENABLED = int(VARS["variables"]["SUB_ENABLED"])
SUB_OAUTH = VARS["variables"]["SUB_OAUTH"]
# Currency
CURRENCY_ENABLED = int(VARS["variables"]["CURRENCY_ENABLED"])
CURRENCY_MINUS = int(VARS["variables"]["CURRENCY_MINUS"])
CURRENCY_VALUE = int(VARS["variables"]["CURRENCY_VALUE"])
UPDATE_CURRENCY = int(VARS["variables"]["UPDATE_CURRENCY"])

USERS = 'bin/users/users.db'
