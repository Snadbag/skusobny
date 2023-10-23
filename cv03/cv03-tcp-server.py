#!/usr/bin/env python3

# Popis protokolu:
# OPERACIA|sprava

# OPERACIE: LOGIN|nick
#           SENDMSG|nick|Ahoj ako sa mas (sprava nemoze obsahovat|)
#           EXIT|nick

MSG_SIZE = 100
USERS = list()

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


sock = s.socket(family=s.AF_INET, type=s.SOCK_STREAM)
sock.bind(("0.0.0.0", 9999))
sock.listen(10)

# navrat = sock.accept()
# client_sock = navrat[0]
# client_addr = navrat[1]

protocol = ChatProtocol("")

while True:
    (client_sock, client_addr) = sock.accept()
    print("Connected client: ({0}:{1}).".format(client_addr[0],client_addr[1]))

    while True:
        client_msg = client_sock.recv(MSG_SIZE)
        protocol.parse(client_msg, USERS)
        
    client_sock.close()

sock.close()

