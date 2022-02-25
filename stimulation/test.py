#!/usr/bin/env python3
# -*- coding: utf-8 -*
# import sys

# import os

# # 得到当前根目录

# o_path = os.getcwd()  # 返回当前工作目录

# address = os.listdir(os.path.abspath(os.path.join(os.getcwd(),
#                                                   "..")))  # 添加上层目录
# print(os.path.abspath(os.path.join(os.getcwd(), '..')))
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
# for i in address:
#     if (os.path.isdir(
#             os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")),
#                          i))):
#         sys.path.append(
# os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), i))

# import web_config
# a = web_config.web_config('127.0.0.1', 100)

import main_process

a = main_process.main_process()
a.stimulating()