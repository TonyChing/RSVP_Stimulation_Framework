#!/usr/bin/env python3
# -*- coding: utf-8 -*

from config.abstract_config_class import abstract_config_class
import main_process
import socket


class StimulationClass(object):
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_stimulation = main_process.main_process()

    def para_load(self, para_config: abstract_config_class):
        '''在加载中采用了访问者模式的构造方法，
        规避了配置不同config文件时行为都不相同导致的代码冗余。
        日后如需要对无人机等新添加功能进行配置则同理即可。
        同时方便在GUI界面做出相应的代码，将应用层代码和配置隔离开。
        '''
        para_config.load_to(self.my_stimulation.para_config)
        return 0

    def image_load(self, image_config: abstract_config_class):
        image_config.load_to(self.my_stimulation.image_config)
        return 0

    def webconfig_load(self, web_config: abstract_config_class):
        web_config.load_to(self.client_socket)
        return 0

    def start(self):
        self.my_stimulation.start(self.client_socket)

    def end(self):
        self.client_socket.close()
        self.my_stimulation.end()
