#!/usr/bin/env python3
# -*- coding: utf-8 -*

import socket
import os
from struct import unpack, pack
import re

from psychopy import visual, core, event
from ctypes import *


class DataAnalysis:
    def __init__(self, data):

        self.__Head = data[0:4].decode()
        self.__Body = b''

        try:
            self.__BodySize = unpack('<I', data[4:8])[0]
            print("CHID:" + str(self.__Head))
            print("BodySize:" + str(self.__BodySize))
        except Exception:
            self.__BodySize = 0

        try:
            if self.__BodySize != 0:
                self.__Body = data[8:8 + self.__BodySize]
        except Exception:
            print("Incomplete Data Received")

    def isStop(self):
        if self.__Head == 'ARED':
            return True

    def getHead(self):
        return self.__Head

    def hasBody(self):
        if self.__BodySize == 0:
            return False
        else:
            return True

    def getBody(self):
        return self.__Body


class main_process(object):
    def __init__(self):
        # 定义Image相关参数 用户使用时从config修改
        self.image_config = {}
        self.image_config[
            'image_address'] = 'D:\刺激电脑硬盘\qinyu\RSVP_python\image'
        self.image_config['image_size'] = [600, 600]
        self.image_config['image_center'] = [200, 400]
        self.image_config['Image_No'] = [1, 2, 1, 2]
        self.image_config['Image_ID'] = [1, 100, 100, 10]

        # 定义实验刺激相关参数
        self.para_config = {}
        self.para_config['trail_number'] = 2
        self.para_config['image_per_trail'] = 100
        self.para_config['stimulation_freq'] = 20

        self.send_book = {
            1: 'CTNS',
            2: 'DCNS',
            3: 'STAR',
            4: 'STOP',
            5: 'STON',
            6: 'SPON',
            7: 'CSAL',
            8: 'SMID'
        }
        self.receive_book = {
            1: 'CTOK',
            2: 'DCOK',
            3: 'TROK',
            4: 'PROK',
            5: 'TNOK',
            6: 'PNOK',
            7: 'CAOK',
            8: 'STSN',
            9: 'RSLT',
            10: 'IMID'
        }

        self.system_state = 'INIT'
        self.exit_flag = False


        self.trigger = CDLL("inpoutx64.dll")
	
        self.mysocket = socket.socket 
        self.BUFSIZE = 15000
    def start(self, mysocket: socket.socket):
        self.mysocket = mysocket
        BUFSIZE = 15000

        while (True):
            if (self.system_state == 'INIT'):

                a = self.send_book[1].encode('utf-8')
                flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                mysocket.send(flow)
                try:
                    data = mysocket.recv(BUFSIZE)
                    data = DataAnalysis(data)
                except Exception:
                    data = b'INIT'
                    data = DataAnalysis(data)
                if data.getHead() == self.receive_book[1]:
                    self.system_state = self.send_book[1]
                    print("CTOK!!!")

            if (self.system_state == self.send_book[1]):
                a = self.send_book[3].encode('utf-8')
                flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                mysocket.send(flow)
                try:
                    data = mysocket.recv(BUFSIZE)
                    data = DataAnalysis(data)
                except Exception:
                    data = b'INIT'
                    data = DataAnalysis(data)
                if data.getHead() == self.receive_book[3]:
                    self.system_state = self.send_book[3]
                    print(self.system_state)
                else:
                    print("Something wrong while connecting")
                    break

            if (self.system_state == self.send_book[3]):
                a = self.send_book[8].encode('utf-8')
                flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                mysocket.send(flow)
                try:
                    data = mysocket.recv(BUFSIZE)
                    while (len(data) < 12000):
                        print(len(data))
                        tt = mysocket.recv(BUFSIZE)
                        data = data + tt
                    data = DataAnalysis(data)

                except Exception:
                    data = b'INIT'
                    data = DataAnalysis(data)
                if data.getHead() == self.receive_book[10]:
                    self.system_state = self.send_book[8]
                else:
                    print(data.getHead())
                    print("Something wrong while connecting")
                    break

            if (self.system_state == self.send_book[8]):

                if data.getHead() == self.receive_book[10]:

                    self.system_state = data.getHead()

                    self.image_config['Image_No'] = list(
                        unpack('<4000B',
                               data.getBody()[0:4000]))

                    self.image_config['Image_ID'] = list(
                        unpack('<4000H',
                               data.getBody()[4000:12000]))

                    a = self.send_book[5].encode('utf-8')
                    flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                    mysocket.send(flow)
                    self.system_state = self.send_book[5]
                else:
                    print(self.system_state)
                    print("Something wrong while connecting")
                    break

            if (self.system_state == self.send_book[5]):
                data = mysocket.recv(BUFSIZE)
                data = DataAnalysis(data)
                if data.getHead() == self.receive_book[5]:

                    self.stimulating()

                    a = self.send_book[6].encode('utf-8')
                    flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                    mysocket.send(flow)
                    self.system_state = self.send_book[6]

                else:
                    print(self.system_state)
                    print("Something wrong while connecting")
                    break

            if (self.system_state == self.send_book[6]):
                data = mysocket.recv(BUFSIZE)
                data = DataAnalysis(data)
                if data.getHead() == self.receive_book[6]:

                    self.system_state = data.getHead()

                    a = self.send_book[4].encode('utf-8')
                    flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                    mysocket.send(flow)
                    self.system_state = self.send_book[4]
                else:
	    
                    print("Something wrong while connecting")
                    break

            if (self.system_state == self.send_book[4]):
                data = mysocket.recv(BUFSIZE)
                data = DataAnalysis(data)
                if data.getHead() == self.receive_book[4]:

                    self.system_state = data.getHead()

                    a = self.send_book[2].encode('utf-8')
                    flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                    mysocket.send(flow)
                    self.system_state = self.send_book[2]
                else:
                    print("Something wrong while connecting")
                    break

            if (self.system_state == self.send_book[2]):
                data = mysocket.recv(BUFSIZE)
                data = DataAnalysis(data)
                if data.getHead() == self.receive_book[2]:
                    a = self.send_book[7].encode('utf-8')
                    flow = pack('<4BI', a[0], a[1], a[2], a[3], 0)
                    mysocket.send(flow)
                    self.system_state = self.send_book[7]
                else:
                    print("Something wrong while connecting")
                    break

            if (self.system_state == self.send_book[7]):
                data = mysocket.recv(BUFSIZE)
                data = DataAnalysis(data)
                if data.getHead() == self.receive_book[7]:
                    try:
                        self.end()
                    except Exception:
                        print("Something wrong while ending")
                else:
                    print("Something wrong while connecting")
                    break

    def end(self):

        core.quit()

    def stimulating(self):
        self.trigger.Out32(0x3100, 0)
        win = visual.Window(fullscr=True,
                            size=(3840, 1600),
                            color=(-1.0, -1.0, -1.0),
                            monitor="test monitor",
                            units="pix")
        win.mouseVisible = False
        # 文字
        pic = visual.ImageStim(win,
                               image=os.path.join(
                                   self.image_config['image_address'],
                                   'warning', '2.jpg'),
                               size=[600, 600])
        pic.draw()
        win.flip()
        core.wait(10)

        text_1 = visual.TextStim(win=win,
                                 text='Stimulation Ready',
                                 height=100,
                                 pos=(0, 100),
                                 bold=True,
                                 italic=False,
                                 color='Blue')

        text_2 = visual.TextStim(win=win,
                                 text='',
                                 height=100,
                                 pos=(0, -200),
                                 bold=True,
                                 italic=False,
                                 color='Blue')
        text_2.text = 'Press Any button to go'

        # 时钟
        timer = core.Clock()

        # 呈现文字刺激
        text_1.draw()
        text_2.draw()
        win.flip()
        core.wait(0)
        timer.reset()  # 重置时间0
        k_1 = event.waitKeys()
        timeUse = timer.getTime()  # 获取时间
        print(k_1, timeUse)
        self.trigger.Out32(0x3100, 6)
        core.wait(0.0001)
        self.trigger.Out32(0x3100, 0)

        dtimer = core.CountdownTimer(4)
        while dtimer.getTime() > 0:
            text_1.text = str(int(dtimer.getTime()))
            text_1.draw()
            win.flip()

        # 图像

        addrwp = os.path.join(self.image_config['image_address'], 'streetwp')
        addrwop = os.path.join(self.image_config['image_address'], 'streetwop')

        image_addr = []
        all_image_number = self.para_config['trail_number'] * self.para_config[
            'image_per_trail']

        for i in range(all_image_number):
            if (self.image_config['Image_No'][i] == 1):
                for j in os.listdir(os.path.abspath(addrwp)):
                    t1 = int(re.split('[_.]', j)[1])
                    t2 = int(self.image_config['Image_ID'][i])
                    if t1 == t2:
                        image_addr.append(os.path.join(addrwp, j))
            else:
                for j in os.listdir(os.path.abspath(addrwop)):
                    t1 = int(re.split('[_.]', j)[1])
                    t2 = int(self.image_config['Image_ID'][i])
                    if t1 == t2:
                        image_addr.append(os.path.join(addrwop, j))

        tt = []
        for i in range(self.para_config['trail_number']):

            pic = visual.ImageStim(win,
                                   image=os.path.join(
                                       self.image_config['image_address'],
                                       'warning', '1.jpg'),
                                   size=self.image_config['image_size'])
            text_2.draw()
            win.flip()
            core.wait(0)
            timer.reset()  # 重置时间0
            k_1 = event.waitKeys()
            pic.draw()
            win.flip()
            core.wait(5)
            time1 = 0
            timer.reset()

            for j in range(self.para_config['image_per_trail']):

                t1 = (i + 1) * (j + 1) - 1
                pic = visual.ImageStim(win,
                                       image=image_addr[t1],
                                       size=self.image_config['image_size'])
                pic.draw()
                win.flip()

                self.trigger.Out32(0x3100, self.image_config['Image_No'][t1])
                core.wait(0.0001)
                self.trigger.Out32(0x3100, 0)

                time1 = timer.getTime()
                tt.append(time1)
                waittime = 1 / self.para_config['stimulation_freq'] - 0.01
                core.wait(waittime)
            #黑屏休息10s
            win.flip()
            core.wait(15)
            #接收RSLT消息
            data = self.mysocket.recv(self.BUFSIZE)
            tdata = DataAnalysis(data)
            while (len(data)<902):
                print(len(data))
                tt = self.mysocket.recv(self.BUFSIZE)
                data = data + tt            
            data = DataAnalysis(data)
            if data.getHead() == self.receive_book[9]:
                print(data.getBody() == 902)
            else:
                print(self.system_state)
                print("Something wrong while connecting")
            
        for i in range(len(tt) - 1):
            tt[i] = tt[i + 1] - tt[i]
        print(tt)
        f = open("log.txt", "w")
        for line in tt:
            f.write(str(line) + '\n')
        f.close()
 
        self.trigger.Out32(0x3100, 8)
        core.wait(0.0001)
        self.trigger.Out32(0x3100, 0)

        win.close()

