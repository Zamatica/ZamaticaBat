# !/usr/bin/env python3
import datetime
import re
import socket

from updates import update, update_mod, get_mods
import connections as con, viewers, mods, editors as edit, background, vars as variable


connect_bot = 0

USERS = 'users/users.db'
start = variable.start

user_mods = get_mods()
user_subs = {}
user_followers = {}
editors = variable.EDITORS
if variable.BROADCASTER in editors:
    pass
else:
    editors.append(str(variable.BROADCASTER))
if variable.NICK in editors:
    pass
else:
    editors.append(str(variable.NICK))


options = {
    '!coin': viewers.command_null, '!quote': viewers.command_quote, '!time': viewers.command_time, '!mods': viewers.send_mod, 'FrankerZ': viewers.frankerz,
}
options_pass = {
    '!help': viewers.command_help, '!run': viewers.command_run, '!stats': viewers.command_stats, '!purchase': viewers.command_purchase
}
options_mod = {
    '!on': mods.command_on, '!runtime': mods.command_runtime, '!ping': mods.command_pong, '!update': update_mod, '!play': mods.command_play_pause, '!next': mods.command_play_next,
    '!prev': mods.command_play_pre, '!addquote': mods.command_quote_add, '!runset': mods.command_run_update, '!check': mods.command_check, '!add': mods.command_add,
}
options_mod.update(options)
options_editor = {'!off': edit.command_off, '!start': edit.editor_command}
options_editor.update(options_mod)


def msg_parse_case(msg):
    if msg[0] == '!help':
        viewers.command_help(sender, user_mods)
    elif msg[0] == '!run':
        viewers.command_run(mods.run)
    elif msg[0] == '!stats':
        viewers.command_stats(sender)
    elif msg[0] == '!uptime':
        viewers.command_uptime(start)
    elif msg[0] == '!purchase':
        con.send_message('Purchase is currently disabled.')


def msg_parse(msg):
    global options
    msg = msg.split(' ')
    if len(msg) >= 1:
        for word in msg[0:50]:
            if word in variable.BANNED_WORDS:
                edit.command_timeout(sender, 1)
            break

        msg_join = " ".join(msg)

        if msg_join.isupper():
            if sender not in user_mods:
                con.send_message("We can hear you just fine @" + sender + ".")

        if len(sender) > 0:
            if msg[0] in options:
                try:
                    options[msg[0]]()
                except KeyError:
                    try:
                        options[msg[0]](msg[1:50])
                    except KeyError:
                        try:
                            options[msg[0]](msg[1], msg[2:50])
                        except KeyError:
                            try:
                                options[msg[0]](msg[1], msg[2], msg[3])
                            except KeyError:
                                try:
                                    options[msg[0]](msg[1], msg[2], msg[3], msg[4])
                                except KeyError:
                                    con.send_message(sender + " - What Command are you using? TypeError - @" + variable.BROADCASTER)
            elif msg[0] in options_pass:
                msg_parse_case(msg)


def msg_parse_mod(msg):
    msg = msg.split(' ')
    global options_mod
    if len(msg) >= 1:
        if len(sender) > 0:
            if msg[0] in options_mod:
                try:
                    options_mod[msg[0]]()
                except TypeError:
                    try:
                        options_mod[msg[0]](msg[1:50])
                    except TypeError:
                        try:
                            options_mod[msg[0]](msg[1], msg[2:50])
                        except TypeError:
                            try:
                                options_mod[msg[0]](msg[1], msg[2], msg[3])
                            except TypeError:
                                try:
                                    options_mod[msg[0]](msg[1], msg[2], msg[3], msg[4])
                                except TypeError:
                                    con.send_message(sender + " - What Command are you using? TypeError - @" + variable.BROADCASTER)
            elif msg[0] in options_pass:
                msg_parse_case(msg)


def msg_parse_editor(msg):
    global options_editor
    msg = msg.split(' ')
    if len(msg) >= 1:
        if len(sender) > 0:
            if msg[0] in options_editor:
                try:
                    options_editor[msg[0]]()
                except TypeError:
                    try:
                        options_editor[msg[0]](msg[1:50])
                    except TypeError:
                        try:
                            options_editor[msg[0]](msg[1], msg[2:50])
                        except TypeError:
                            try:
                                options_editor[msg[0]](msg[1], msg[2], msg[3])
                            except TypeError:
                                try:
                                    options_editor[msg[0]](msg[1], msg[2], msg[3], msg[4])
                                except TypeError:
                                    con.send_message(sender + " - What Command are you using? TypeError - @" + variable.BROADCASTER)
            elif msg[0] in options_pass:
                msg_parse_case(msg)


data = ""
BOT_ENABLED = 1
temp_mod = []


def restart():
    print("-- WARNING[IRC]: Socket timeout")
    string_start = input("-- SYSTEM: Attempt a Restart? (Y/N)   ")
    yes = {'yes', 'YES', 'y', 'Y', '+'}
    no = {'no', 'NO', 'n', 'N', '-'}
    if string_start in yes:
        print("-- BOT: Attempting Restart...")
    elif string_start in no:
        print("-- SYSTEM: Exiting...")
        exit()


def startup():
    background.command_start_all()
    print("")
    print("-- BOT: Version 1.5")
    print("-- BOT: Connected and Ready.")
    print("")
    print("Running Updates...")
    update()
    print("Updates Finished")
    print("Current moderators: " + str(user_mods))
    print("")
    con.send_message("Connected to " + variable.USER + ".")
    edit.editor_command()
    mods.mod_commands()
    viewers.viewer_commands()
    con.send_message("/TWITCHCLIENT 3")


startup()

conn = con.connection

while True:
    try:
        data = data+conn.recv(1024).decode('utf-8')
        data_split = re.split(r"[~\r\n+]", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)
            if len(line) >= 1:
                try:
                    if line[0] == 'PING':
                        con.send_pong(line[1])
                    elif line[1] == 'PRIVMSG':
                        sender = con.get_sender(line[0])
                        message = con.get_message(line)

                        if sender in editors:
                            msg_parse_editor(message)
                            print(sender + "[EDITOR]: " + message)
                        elif sender in user_mods:
                            msg_parse_mod(message)
                            print(sender + "[MOD]: " + message)
                        else:
                            msg_parse(message)
                            if sender in user_followers:
                                print(sender + "[FOL]: " + message)
                            elif sender in user_subs and variable.SUB_ENABLED == 1:
                                print(sender + "[SUB]: " + message)
                            else:
                                print(sender + ": " + message)
                except IndexError:
                    # catches ~ to not error
                    pass
    except socket.error:
        print("-- IRC: Cannot Read Chat")
        print("-- CRITICAL: Socket Closed | Error.")
        restart()
    except socket.timeout:
        print("-- IRC: Cannot Read Chat")
        print("-- CRITICAL: Socket Closed | Timeout.")
        restart()
