# !/usr/bin/env python3
import sqlite3
import json
import webbrowser as wb
from sys import exit
from os import remove, system
from time import sleep
system("mode con: cols=200 lines=65")
print("")
print("Welcome to setup. The Guide will now prompt you.\n")
print("Some things are 1 or 0   |   1 means Yes and 0 means No. \n")


def json_write(section, field, value):
    with open('bin/config/vars.json', 'r+') as settings_file:
        settings = json.load(settings_file)

        settings[section][field] = value

        settings_file.seek(0)
        settings_file.write(json.dumps(settings, indent=2, sort_keys=True))
        settings_file.truncate()


def ban_words_parse(banned_words):
    with open('bin/config/vars.json', 'r+') as settings_file:
        settings = json.load(settings_file)
        words = banned_words.split(',')
        main = settings["variables"]["BANNED_WORDS"]
        final_list = []
        for word in words:
            if word not in main:
                final = word.replace(" ", "")
                print(final + " added.")
                final_list.insert(0, final)
            else:
                print(word + " is already in the list.")

        for item in final_list:
            main.insert(0, item)

        settings_file.seek(0)
        settings_file.write(json.dumps(settings, indent=2, sort_keys=True))
        settings_file.truncate()

    print(main)


def sql():
    sql_clear = input("Are you sure? (Y/N)")
    if sql_clear.upper() in ['Y', 'YES']:
        remove('bin/user/users.db')
        conn = sqlite3.connect('user/users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE `users` (
                `ID`	INTEGER UNIQUE,
                `name`	TEXT UNIQUE,
                `gold`	REAL DEFAULT 0,
                `timeouts`	INTEGER DEFAULT 0,
                `mod`	INTEGER DEFAULT 0,
                `follower`	INTEGER DEFAULT 0,
                `sub`	INTEGER DEFAULT 0,
                PRIMARY KEY(ID)
            );
        ''')
        print("New Database Created.")
        print("Settings Finished. Have Fun!")
        sleep(3)
        exit()
    else:
        exit()


def json_reset():
    with open('bin/config/vars.json', 'w') as settings_file:
        default = '{"connection":{"HOST":"irc.twitch.tv","PORT":"6667","CHAN":"","NICK":"","PASS":""},"variables":{"BROADCASTER":"","TIMEZONE":"","TIMEOUT_TIME":"45","TIMEOUT_LIMIT":"3","UPDATE":"60.0","FOL":"0","BANNED_WORDS":["niggers","nigger","faggot","niggas","nigga","niqqa","niqqas"],"OPTIONAL":"NULL","SUBS":"0","SUB_OAUTH":"","MUSIC_ENABLED":"0","BROADCAST_ENABLED":"0","BROADCAST":"","BROADCAST_SHOWN":"60.0","MEDIA_ENABLED":"0","TITLE":"None","TITLE_SHOWN":"75.0","SOCIAL_MEDIA":"None","MEDIA_SHOWN":"180.0","CURRENCY_ENABLED":"0","CURRENCY_MINUS":"20","UPDATE_CURRENCY":"3600","CURRENCY_VALUE":"15","WINDOW_SIZE":"300"}}'
        def_read = json.loads(default)
        json.dump(def_read, settings_file, sort_keys=True, indent=2, ensure_ascii=False)
        print("Reset without error. Yay!")
        sleep(2)
x = input("Do you want to run setup or other action? \nY -runs setup\nN -exits\nClearDB -clears the database\nResetJson (rj) -resets the JSON file to default. \n\n")
print('')
if x.upper() in ['Y', 'YES']:
    with open('bin/config/vars.json', 'r') as VARS:
        channel = input("Your Channel name (Not the Bot's Username): \n")
        json_write('connection', 'CHAN', '#'+str(channel).lower())
        json_write('variables', 'BROADCASTER', str(channel).lower())
        print('')
        bot_name = input("Bot's twitch username? \n")
        json_write('connection', 'NICK', str(bot_name))
        print('')
        password = input("oAuth Pass (You can copy/paste it here): \n")
        json_write('connection', 'PASS', str(password))
        print('')
        editors = input("Put any channel editors here separate by a comma (Don't include you or bot): \n")
        editors = editors.split(',')
        editors = [editor.replace(' ','') for editor in editors]
        json_write('variables', 'EDITORS', editors)
        print('')
        timezone = input("Timezone?: \n")
        json_write('variables', 'TIMEZONE', str(timezone).upper())
        print('')
        ban_words = input("Banned Words: Words you don't want on the chat, separate with a comma. Hit Enter for default. \n")
        ban_words_parse(ban_words)
        print('')
        subs = input("If you have subs and want to enable them please refer here: https://github.com/Zamatica/ZamaticaBat/#streaming. Enter 1 to go there now. \n")
        if subs == '1':
            wb.open('https://github.com/Zamatica/ZamaticaBat/#streaming')
        print('')
        fol = input("Do you want to record followers (1/0)? (Performance Reductions) \n")
        json_write('variables', 'FOL', str(fol))
        print('')
        music = input("Music Enabled? (1/0) \n")
        json_write('variables', 'MUSIC_ENABLED', str(music))
        print('')
        broadcast = input("Broadcast info in chat? (1/0) \n")
        json_write('variables', 'BROADCAST_ENABLED', str(broadcast))
        if broadcast == '1':
            broadcast_message = input("Display what text? (You can copy/paste - Hit Enter to Disable.) \n")
            json_write('variables', 'BROADCAST', str(broadcast_message))
        print('')
        media = input("Display Social Media? (1/0) \n")
        json_write('variables', 'MEDIA_ENABLED', str(media))
        if media == '1':
            media_message = input("Display what social media? (You can copy/paste - Hit Enter to Disable.) \n")
            json_write('variables', 'SOCIAL_MEDIA', str(media_message))
            print('')
        title_enable = input("Display a title message in chat? (1/0) \n")
        if title_enable == '1':
            title = input("Display what title? (You can copy/paste - Hit Enter to Disable.) \n")
            json_write('variables', 'TITLE', str(title))
        print('')
        currency = input("Enable Currency? (1/0) \n")
        json_write('variables', 'CURRENCY_ENABLED', str(currency))
        print('')
        print('')
        sql_input = input("Create New Database? (1/0) \n")
        if sql_input == '1':
            sql()
            print("Settings Finished. Have Fun! You can close me now.")
        print('')
        print("Settings Finished. Have Fun! You can close me now.")
        VARS.close()
        sleep(10)
        exit()
elif x.upper() == 'CLEARDB':
    sql()
elif x.lower() in ['resetjson', 'rj']:
    json_reset_yn = input("Are you sure? (Y/N)\n")
    if json_reset_yn.lower() == 'y':
        json_reset()
    else:
        print("Exiting...")
        sleep(1)
        exit()
elif x.upper() in ['N', 'NO']:
    print("Exiting...")
    sleep(1)
    exit()
else:
    print("Not a command. Restart")
    sleep(1)
    exit()
