#coding time:20.Feb
#一个简单的文件查找功能

import os
import os.path
global target_list
target_list = []
# 创建一个列表用来储存目标文件的路径

def file_seek(file_path,keyword):
    file_list = os.listdir(file_path)
    #获取file_path下所有文件（文件夹）
    for file_name in file_list:
        file_path_temp = os.path.join(file_path, file_name)
        #将当前路径与文件名或子路径合在一起,开辟一个新空间path_temp储存，不能直接赋值，避免在嵌套后影响原参数传值
        # print(file_path_temp)
        if os.path.isdir(file_path_temp):
            #如果是子路径，嵌套查找过程
            file_seek(file_path_temp,keyword)
        else:
            #如果是文件
            if file_path_temp.find(keyword):
                global target_list
                # 全局变量使用前申明
                target_list.append(file_path_temp)

def Main():
    file_path = input("输入要搜索的路径：\n")
    keyword = input("输入要查找的文件关键字：\n")
    file_seek(file_path,keyword)
    print(target_list)

Main()

'''
测试中建立了一个这样的多级文件夹。文件排列顺序自上而下。
                             c  -  book.txt
                          /
                       a  - book.txt
                   /
D： -  skl_temp    -   b  - book.txt
                   ╲ 
                     book.txt 

输入要搜索的路径：
D:\skl_temp
输入要查找的文件关键字：
book
print :
['D:\\skl_temp\\a\\book.txt',
 'D:\\skl_temp\\a\\c\\book.txt', 
 'D:\\skl_temp\\b\\book.txt', 
 'D:\\skl_temp\\book.txt']
 
 
在15行处加入一个Print，得到如下结果

D:\skl_temp\a
D:\skl_temp\a\book.txt
D:\skl_temp\a\c
D:\skl_temp\a\c\book.txt
D:\skl_temp\b
D:\skl_temp\b\book.txt
D:\skl_temp\book.txt

可以看到.listdir的排列顺序有点奇怪，在文件夹a中，先输出了book.txt，后遍历\a\c，即先文件，后目录
而在父文件夹\skl_temp中，book.txt反而顺序是在最后。

考虑可能是由于命名的关系，a>b>c>d... 将book.txt改为duck.txt后，得到如下结果
D:\skl_temp\a
D:\skl_temp\a\c
D:\skl_temp\a\c\duck.txt
D:\skl_temp\a\duck.txt
D:\skl_temp\b
D:\skl_temp\b\duck.txt
D:\skl_temp\duck.txt

在文件a中，先遍历到了\a\c，后得到duck.txt。
即listdir的排列顺序与文件属性无关，与命名方式相关。

另外Python对于处理嵌套函数，会先将嵌套部分执行完后，再执行后续其他内容。

'''