# !/usr/bin/env python3
import socket
import config.variable as variable

connection = socket.socket()
connection.connect((variable.HOST, variable.PORT))


def send_pong(msg):
    connection.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(msg, chan=variable.CHAN):
    connection.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))
    print(" == [BOT] " + variable.NICK.upper() + ": " + msg)


def whisper(msg, chan=variable.CHAN_WHISPER):
    connection.send(bytes('WHISPER %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    connection.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    connection.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    connection.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    connection.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


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
