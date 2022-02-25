# RSVP_python刺激系统说明文档

[TOC]

## RSVP_python工程各文件夹说明

### config

config文件夹内提供对外的配置文件接口，目前有web_config——配置ip和port，image_config——配置在RSVP显示过程中刺激图片的地址、图片大小、显示位置（当前程序锁死在屏幕中央）、显示的图像的顺序及其是否为目标图，para_config——配置在刺激过程中需要几轮实验、每组实验显示几张图片以及显示刺激的频率。

### image

存放刺激图片的文件夹。目前streetwop是非目标图，streetwp是目标图，warning是一些提示用的图。

### stimulation

存放刺激工程主体代码的文件夹。main_process是具体编程各个环节都在做什么的文件——包括网络连接收发处理、图像刺激显示（psychopy）等等，stimulation_class是对外提供的抽象接口方便main函数调用（main函数应该只与此class以及config文件交互）。



当前运行效果为运行后先进行网络连接，然后进入到main_process的start函数进行通信，等处理端传来显示的图像的顺序及其是否为目标图（Image_No\ID）进行保存并且开始刺激，刺激用psychopy书写。每刺激一轮开始前都会要求用户按下任意键，之后显示5s的视觉提示图，随后开始刺激，结束后黑屏10s作为休息，同时等待处理端发回处理结果（现在未对其进行处理，只是接收了），如此循环。



注意psychopy使用时需要针对当前屏幕分辨率修改程序中的参数。



## 技术实现要点说明

### 用户端使用说明

main.py 中 调用config中定义的不同config文件，进行加载。之后只需要进行stimulation.start() 和 end()即可。

全部配置工作都应该在config中完成。若需要更改具体逻辑则更改main_process.py即可。 

### 书写代码规则

整个文件中的代码尊从以下规则：

1. 除函数内参外其余情况运用 = 时，左右必须各空一格。

2. 函数参数书写时逗号后必须空一格。

3. 每个.py文件下必须有 if \_\_name\_\_ ==  '\_\_main\__' :  判定，进行相应处理。

4. 命名统一采用如下风格。

   | 类别                       | Public(常见用法)        | Internal（类内函数）            |
   | :------------------------- | ----------------------- | ------------------------------- |
   | Packages                   | package_name            |                                 |
   | Modules                    | module_name             | _module_name                    |
   | Classes                    | ClassName               | _ClassName                      |
   | Exceptions                 | ExceptionName           |                                 |
   | Functions                  | function_name()         | _function_name()                |
   | Global/Class Constants     | GLOBAL_CONSTANT_NAME    | _GLOBAL_CONSTANT_NAME           |
   | Global/Class Variables     | global_var_name         | _global_var_name                |
   | Instance Variables         | instance_var_name       | _instance_var_name()(protected) |
   | Method Names               | method_name()           | _method_name()(protected)       |
   | Function/Method Parameters | function_parameter_name |                                 |
   | Local Variables            | local_var_name          |                                 |

5. 必须使用 `if foo:` 而不是 `if foo != []:` 作为判定foo非空或非0的条件。

6. 对列表操作后必须判断列表是否为空（帮助检查是否有误）

   ```python
   if not a: # a = []
       print("a is [] Empty")
   else:			# a = [list_in_here]
       print("Do your work here")
   ```

7. 所有导入文件操作应该位于文件顶部，禁止使用局部导入(如函数内部使用import)。

8. 所有包外模块均不在\_\_init\_\_文件中进行提前导入，防止阅读各代码时不知道导入模块。\_\_init\_\_文件可用来定义version author等信息，并提供\_\_all\_\_ 定义（在上层代码使用from xx import *时有效）。

   该文件是Python中package的标识，不能删除。

   ```python
   # 以下是__init__文件 在xx文件夹下
   from __future__ import absolute_import
   
   __all__= ['conf','preprocess','myplot'] #（本文件夹内的.py文件会被导入）
   ```

9. 绘图时必须有完整坐标轴标注。 

10. try except只有在能够自我清楚什么样的exception会发生时才能使用。

11. 缩进 1 Tab = 4 space 。

12. 禁止将两个class放到一个文件中。

base.h 定义了整个工程中需要用到的数据结构的接口，存放在db_compress命名空间下。

### config文件

在配置config时使用了访问者模式，这样可以灵活的改动未来可能删改添的功能所需要的配置，缺点是在增加一个新的config时需要改动stimulation_class，并且config需要对被访问类的代码熟悉（这样才能load_to()）。

abstract_config_class定义了抽象的config文件，保证所有config文件都是单例模式运行（就像一个电脑只有一个回收站实体）在整个文件夹内任何地方调用了具体的config文件都以最近都那次实例化的配置为主。



### stimulation_class文件

本文件中应该包含所有用户（main.py）可能执行的动作。如果需要添加GUI，只需要对应绑定本类中的一个方法即可。config文件的“访问者模式”在这个类里得到体现。



### 未来添删改

config（改配置）、main_process（改具体功能的逻辑）、stimulation_class（增加新的功能）、main.py(改变用户端的逻辑)。

