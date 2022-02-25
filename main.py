#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
This is main.py contains function of calculating TeacherStudentRatio
and the main() execution code.
| AUTHOR |    UPDATE   |   EMAIL                    |
| QinYu  |  2020/10/01  | contact:qinyu@pku.org.cn   |

TODO:
    (QinYu)1 The stimulation time can vary from computer to computer. We need to add a calibration function.
	(see main_process.py waittime = 1 / self.para_config['stimulation_freq'] - 0.01 and log.txt file then u will understand)
	2 no trigger function right now.
KLUDGE:
    The code where is currently using stupid method,
    but can have a better way to do so if you have the time.
    (QinYu)image config and para config currently need to be changed in both config folder and main_process.py, waiting to be fixed.
Tricky:
    Hard-to-understand parts of code.
'''
# system import
import os
import sys
address = os.listdir(os.path.abspath(os.getcwd()))
for i in address:
    if (os.path.isdir(os.path.join(os.path.abspath(os.getcwd()), i))):
        sys.path.append(os.path.join(os.path.abspath(os.getcwd()), i))
# project import
from stimulation.stimulation_class import StimulationClass
import web_config
import image_config
import para_config
# 会引起PEP 8 格式错误，解决方案 利用setup.py将当前python文件安装至本地即可随便import

# local import


def main():

    # 设计如下用户代码是为了方便改成GUI交互方式进行配置以及开始刺激
    stimulation_controller = StimulationClass()
    # stimulation_controller.para_load(config.stimulation_config)
    # stimulation_controller.image_load(config.image_config)

    web = web_config.web_config('192.168.1.2', 9095)
    image = image_config.image_config()
    para = para_config.para_config()
    stimulation_controller.webconfig_load(web)
    stimulation_controller.para_load(para)
    stimulation_controller.image_load(image)
    try:
        stimulation_controller.start()
        flag = 0
    except Exception as e:
        print(str(e))
        print("Start Stimulation Failed")
        flag = 1

    if (flag == 0):
        stimulation_controller.end()

    return 0


if __name__ == '__main__':
    main()
