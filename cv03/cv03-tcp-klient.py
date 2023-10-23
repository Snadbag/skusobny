#!/usr/bin/env python3

import socket as s

class ChatProtocol:
    def __init__(self, nick):
        self._nick = nick
    
    def login(self):
        return "LOGIN|{}".format(self._nick).encode()
    
    def exit(self):
        return "EXIT|{}".format(self._nick).encode()
    
    def send_msg(self, msg):
        return "SENDMSG|{}|{}".format(self._nick, msg).encode()
    
    def parse(self, bin_msg, user_list):
        str_msg = bin_msg.decode()
        list_msg_parts = str_msg.split("|")

        if list_msg_parts[0] == "LOGIN":
            user_list.append(list_msg_parts[1])
        
        elif list_msg_parts[0] == "EXIT":
            user_list.remove(list_msg_parts[1])

        elif list_msg_parts[0] == "SENDMSG":
            print("Client '{}' msg: {}".format(list_msg_parts[1],
                                                list_msg_parts[2]))

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

sock = s.socket(family=s.AF_INET, type=s.SOCK_STREAM)
sock.connect( (SERVER_IP, SERVER_PORT) )

nick = input("Enter nick: ")
protocol = ChatProtocol(nick)
sock.send(protocol.login())

while True:
    msg = input("Enter message: ")

    if msg[0] == "%":
        if msg[1] == "q":
            sock.send(protocol.exit())
            sock.close()
            exit(0)

    sock.send(protocol.send_msg(msg))

