# !/usr/bin/env python3
import datetime
import linecache
import random
import sqlite3
from users.updates import get_mods

from systems.background import sql_timeout
import systems.connections as con
import config.variable as variable


USERS = variable.USERS

send_message = con.send_message


def offense(sender, user_mods):
    if sender not in user_mods:
        print(sender + " has made on offense.")
    return sql_timeout(sender)


def offense_auto(sender):
    print(sender + " has made on offense.")
    return sql_timeout(sender)


def command_null():
    pass


def command_help(sender, user_mods):
    send_message('There is !help, !ping, !uptime, !time, !stats, !run, !coin, and !test.')
    if sender in user_mods:
        send_message('Mod: !runset, !on, !admin, !runtime, !ping, !addquote, !p(n/p), and !update.')


def command_nonadmin_off(sender):
    send_message("No. You are not the broadcaster, " + sender + ".")


def command_uptime(start):
    now = datetime.datetime.now()
    timepass = now - start

    total_seconds = int(timepass.total_seconds())
    hours, remainder = divmod(total_seconds, 60*60)
    minutes, seconds = divmod(remainder, 60)

    send_message('{} hrs {} mins {} secs'.format(hours, minutes, seconds))


def command_time():
    now = datetime.datetime.now()
    send_message(str(now)[0:19] + " " + variable.TIMEZONE)


def command_test():
    send_message('Testing stuff')  # command to test if working, can use !on


def command_purchase(item, quantity, sender):

    conn = sqlite3.connect(USERS)

    c = conn.cursor()

    if variable.CURRENCY_ENABLED == 9:
        if item == 'timeout':
            item_buy = 'timeout'
            for timeout in c.execute("SELECT ? FROM users WHERE name LIKE ?", [item_buy, sender]):
                timeouts = timeout[0]
                if timeouts > 0:
                    for stats in c.execute("SELECT currency FROM users WHERE name LIKE ?", [sender]):
                        if stats[0] >= (variable.CURRENCY_VALUE*4)*int(quantity[0]):
                            c.execute("UPDATE users SET currency = currency - ? WHERE name = ?;", [variable.CURRENCY_VALUE*4*int(quantity[0]), sender])
                            c.execute("UPDATE users SET timeout = timeout - ? WHERE name = ?;", [quantity[0], sender])
                            conn.commit()
                            for stats_new in c.execute("SELECT currency FROM users WHERE name LIKE ?", [sender]):
                                for timeout_new in c.execute("SELECT ? FROM users WHERE name LIKE ?", [item_buy, sender]):
                                    send_message("{}, you have purchased a warning removed. You now have ${} and {} timeouts".format(sender, stats_new[0], timeout_new[0]))
                                    break
                                break
                        else:
                            send_message(sender + ", you do not have enough.")
                        break
                else:
                    send_message(sender + ", you have 0 timeouts.")
                break
    else:
        send_message("Currency Disabled")
    conn.commit()
    conn.close()


def command_coin(cmd='help', amount='01', name='01'):
    conn = sqlite3.connect(USERS)
    c = conn.cursor()
    if variable.CURRENCY_ENABLED == 1:
            add = {'add', 'plus', '+'}
            sub = {'sub', 'subtract', '-'}
            if cmd == 'help':
                send_message("!coin has add, subtract, and set. !coin <cmd> <amount> <name>")
            elif cmd in add:
                c.execute("UPDATE users SET currency = currency + (?) WHERE name LIKE (?)", [amount, name])
                conn.commit()
                for value in c.execute("SELECT currency FROM users WHERE name LIKE ?", [name, ]):
                    send_message(name + " now has $" + str(value[0]) + ".")
            elif cmd in sub:
                c.execute("UPDATE users SET currency = currency - ? WHERE name LIKE ?", [amount, name])
                conn.commit()
                for value in c.execute("SELECT currency FROM users WHERE name LIKE ?", [name, ]):
                    send_message(name + " now has $" + str(value[0]) + ".")
            elif cmd == 'set':
                c.execute("UPDATE users SET currency = ? WHERE name LIKE ?", [amount, name])
                conn.commit()
                for value in c.execute("SELECT currency FROM users WHERE name LIKE ?", [name, ]):
                    send_message(name + " now has $" + str(value[0]) + ".")
    else:
        send_message("Currency Disabled.")

    conn.close()


def command_quote():
    number = random.randint(0, len(open('systems/quotes.txt').readlines())+1)
    try:
        quotes = 'config/quotes.txt'
        line_quote = linecache.getline(quotes, number)
        if line_quote != '':
            send_message(line_quote)
        else:
            send_message("Quote Error: Cannot choose from an empty sequence. Add quotes.")
            print("-- ERROR: IndexError, Cannot choose from an empty sequence. Add quotes.")
    except IndexError:
        send_message("Quote IndexError: Cannot choose from an empty sequence. Add quotes.")
        print("-- ERROR: IndexError, Cannot choose from an empty sequence. Add quotes.")
        print(number)
    except KeyError:
        command_quote()


def command_stats(sender):
    conn = sqlite3.connect(USERS)
    c = conn.cursor()
    name_check = list(map(lambda x: x[0], c.execute("SELECT * FROM tableOut WHERE name LIKE ?", [sender])))
    if sender in name_check:
        for stats in c.execute("SELECT currency FROM tableOut WHERE name LIKE ?", [sender]):
            for offenses in c.execute("SELECT timeout FROM tableOut WHERE name LIKE ?", [sender]):
                if variable.CURRENCY_ENABLED == 0:
                    send_message(sender + ", " + str(offenses[0]) + " offenses.")
                if variable.CURRENCY_ENABLED == 1:
                    send_message(sender + ", you have $" + str(stats[0]) + " and " + str(offenses[0]) + " offenses")
                break
            break
    else:
        send_message("@" + sender + ", you are not found in the USERS.")
    conn.commit()
    conn.close()


def send_mod():
    send_message(get_mods())


def command_run(run):
    send_message(run)


def frankerz():
    send_message("FrankerZ")


def viewer_commands():
    send_message("Viewer Loaded.")
