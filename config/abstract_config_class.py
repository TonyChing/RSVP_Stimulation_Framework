#!/usr/bin/env python3
# -*- coding: utf-8 -*

from abc import ABC, abstractmethod
import threading


class singleton(object):
    '''单例模式
    在程序任何地方只会有一个实例化的类实体。
    保证全局各处使用的config文件统一
    '''
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance_dict'):
            singleton.instance_dict = {}

        if str(cls) not in singleton.instance_dict.keys():
            with singleton._instance_lock:
                _instance = super().__new__(cls)
                singleton.instance_dict[str(cls)] = _instance

        return singleton.instance_dict[str(cls)]


class abstract_config_class(ABC, singleton):
    @abstractmethod
    def load_to(self):
        '''abstractmethod修饰抽象类
        抽象类必须在继承后进行完成
        '''
        pass
