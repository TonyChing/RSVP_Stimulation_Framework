#!/usr/bin/env python3
# -*- coding: utf-8 -*

# configuration of the tcpip connection
import abstract_config_class
import socket


class web_config(abstract_config_class.abstract_config_class):
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT


    def load_to(self, my_socket: socket.socket):
        my_socket.connect((self.IP, self.PORT))
        return 0
