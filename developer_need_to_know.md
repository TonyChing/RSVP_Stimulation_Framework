# 代码风格

参考如下：

所有人的代码都应尊统统一种编程风格，在这建议使用Google Python风格。

Google Python风格指南：  
- [指南原文](https://google.github.io/styleguide/pyguide.html)
- [中文翻译版](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/)

这里有个风格化的工具YAPF，各位可以搜索使用一下。

init import相关知识：https://www.cnblogs.com/byronsh/p/10745292.html

需要发布成可pip install时参考：https://zhuanlan.zhihu.com/p/73199573



本项目必须遵守：

1. 除函数内参外其余情况运用 = 时，左右必须各空一格。

2. 函数参数书写时逗号后必须空一格。

3. 每个.py文件下必须有 if \_\_name\_\_ ==  '\_\_main\__' :  判定，进行相应处理。

4. 命名统一采用如下风格。

   | 类别                        | Public(常见用法)          | Internal（类内函数）            |
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

     

# 完善的docstring及注释
参考如下：
- Google Python编码规范 - 注释和docstring节：https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings。

本项目必须遵守：

1  不论在何处书写所有代码必须分段书写。每段上方用#注释添加一段注释解释代码用途，段后空一行。必要时可在任何代码后添加#进行简短说明。所有#后注释都应该空一格再进行书写。      

2  所有函数及类需要添加docstring ''' ''' 说明。

3  注释不需要描述代码，要解释代码（假设代码大家都能读懂，解释作用即可）。

4  一般情况下一个文件夹(package)最多只有一个文件执行main()。

5  在执行文件(main.py)中必须添加项目相关信息。

6  在每个.py文件上方可以选择性添加该文件相关信息的注释块（如修改日期及人员及其联系方式）。



一个例子：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
This is main.py contains function of calculating TeacherStudentRatio
and the main() execution code.
| AUTHOR |    UPDATE   |   EMAIL                    |
| QinYu  |  2020/9/18  | contact:qinyu@pku.org.cn   |

TODO: 
    (QinYu)Extend the function to an abstract class.
KLUDGE: 
    The code where is currently using stupid method, but can have a better way to do so if you have the time.
Tricky: 
    Hard-to-understand parts of code.
'''
#system import
import os
import sys
import traceback

#project import
import pandas as pd

#local import
from AsdEyeTrackingDataAnalysis.data_preprocess import *

#下面这段函数应该放在另一个文件，这里方便演示
def teacher_student_ratio(number_of_teacher, number_of_student) -> float:
    '''Calculating TeacherStudentRatio. 
    
    Ratio = TeacherNum:StudentNum
    
    Args:
        number_of_teacher: The student number, should be int>0.
        number_of_student: The student number, should be int>0

    Returns:
        Ratio of Teacher:student. Should be float>0.0
        0.5 means Teacher:student = 1:2
        
        Return Example:
        0.3 

    Raises:
        Error: 输入必须为大于0的整数.
        
    Usage:
    >>> ans = teacher_student_ratio(6,3)
    >>> print(ans)
    >>> 2
    '''
    if((number_of_teacher<=0) or (number_of_student<=0) or\
       not isinstance(number_of_student,int)or not isinstance(number_of_teacher,int)):
        raise Exception("输入必须为大于0的整数.当前学生为{0},老师为{1}".format(number_of_teacher,number_of_student))
    ratio = number_of_teacher/number_of_student
    return ratio
#一直到这里应该在另一个文件中 main文件应该只有main函数。

def main():
    #以下实例如何书写不会卡死（使用中弹出错误）的程序
    while(True):
        try:
            number_of_teacher = int(input("number of teacher:"))
            number_of_student = int(input("number of student:"))
            ans = teacher_student_ratio(number_of_teacher,number_of_student)
            break
        except Exception as e:
            print(e)        
    print("Ratio: %f" %ans)
    return 0

if __name__ =='__main__':
    main()
```

```python
运行如下：
number of teacher:0
number of student:-1
输入必须为大于0的整数.当前学生为-1,老师为0
number of teacher:2.3
invalid literal for int() with base 10: '2.3'
number of teacher:2
number of student:2
Ratio: 1.000000
```



# 分支开发
主要思想就是，维护主分支的稳定性，各个成员在各自的分支上开发，定期merge到主分支上。

# 测试(暂无需求)
可参考或者使用numpy的测试框架：https://numpy.org/doc/stable/reference/routines.testing.html

暂时需要时简单使用assert进行测试即可。文件命名test_my_funcion.py

# 完善的文档
开发过程中，以wiki或者README的形式记录下关键事项。  
比如开发规划，排期，主分支的更新记录等等

README.md用来说明各个模块作用以及更新时间及人员信息

LICENSE 开源或上线前再弄也来得及