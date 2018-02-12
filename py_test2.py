#coding time:11-12.Feb
#制作一个简单的成绩录入与查询系统
#不熟悉py，已知可改进的：
#1.可以在函数内部抛出异常弹出
#2.图方便将文件打开关闭写在了函数内，造成了不必要的多次文件开关


import os
global check_stu
check_stu = 0

def Grade_input():
    #数据输入并将信息保存到当前工程路径下的txt文本中
    file_stu = open("grade.txt", "w")
    i = 1
    print("开始输入学生信息，以空格间隔，回车确认。单独输入Q退出。")
    while 1:
        Uinfo_stu = input("请输入第%d个学生信息，依次输入姓名、学号、各科成绩：" %(i))
        if Uinfo_stu == 'Q':
            break
        else:
            file_stu.write(Uinfo_stu + '\n')
        i += 1
    file_stu.close()

def Stu_add():
    #不修改数组，通过文件操作添加。
    file_stu = open("grade.txt", "a+")
    print("开始录入新学生的信息，以空格间隔，回车确认。单独输入Q退出。")
    while 1:
        info_stu = input("请依次输入姓名、学号、各科成绩：")
        if info_stu == 'Q':
            break
        else:
            file_stu.write(info_stu + '\n')
    print("------------新信息录入成功------------")
    file_stu.close()

def Grade_read():
    file_stu = open("grade.txt", "r")
    info_stu = file_stu.readlines()
    grade_2d = []
    # 建立二维列表储存所有学生信息
    for line in info_stu:
        list_stu = (line.split())
        # 建立临时一维列表储存各个学生信息，好奇PY里有没有free释放临时变量的内存。
        grade_2d.append(list_stu)
    print("------------成功读入学籍信息------------\n")
    print(grade_2d)
    file_stu.close()
    return grade_2d

def Newgrade_add(grade_2d):
    print("请输入新科目的成绩")
    i = 0
    for line in grade_2d:
        print(grade_2d[i][0] + ":")
        new_grade = input()
        grade_2d[i].append(new_grade)
        i += 1
    print("------------录入新科目成绩完毕------------")

def Savechange(grade_2d):
    file_stu = open("grade.txt", "w+")
    for line in grade_2d:
        for item in line:
            file_stu.write(str(item))
            file_stu.write(' ')
        file_stu.write("\n")
    #无法将列表直接写入TXT文档，如果直接str(list)会将[‘’]一起录入TXT，十分不便。
    #用json格式似乎可以完美避免这个问题，晚点再研究。这里先使用二次循环将数据一项项的录入进TXT。
    file_stu.close()
    print("------------保存成功------------")

def Datacheck():
    if os.path.exists("grade.txt") != True:
        print("学籍档案不存在，请先建立学籍档案")
    return os.path.exists("grade.txt")

def Stu_del(grade_2d,index):
    if grade_2d[index]:
        del grade_2d[index]
        print("删除该生学籍成功")

def Stu_seek(grade_2d):
    idn_stu = input("请输入想查找的学生学号:")
    index = 0
    global check_stu
    check_stu = 0
    #重置check_stu判断存在性
    line_count = len(grade_2d)
    for index in range(line_count):
    #另一种更好的写法，for line in grade_2d.
    #这里还是把这种写法留着学习
        if idn_stu in grade_2d[index]:
            print("该学生信息如下：")
            print(grade_2d[index])
            check_stu = 1
            break
        if index == line_count - 1:
            print("不存在该学生。")
            break
    return index

def Grade_avg(grade_2d):
    list2d_gradeavg = []
    # 由于直接更新在原二维列表后，会出现加入新成绩的之后，平均分与单科分数分不清的情况。
    # 因此用额外的一个二维列表独立储存平均分，加权平均分，绩点等统计信息
    # 相比放在一起不仅占用了更多的内存，并且看起来十分的蠢。但是现在懒得改进了，也许这就是菜鸡把
    # 后续改进考虑可将平均分等统计信息放置队末，后续单科分数利用insert加入。
    for line in grade_2d:
        index = 0
        grade_sum = 0
        list1d_gradeavg = []
        for item in line:
            if index < 2:
                list1d_gradeavg.append(item)
            if index >= 2:
            #前两项为姓名学号，pass掉
                grade_sum += int(line[index])
            index += 1
        grade_avg = grade_sum / (index - 2)
        list1d_gradeavg.append(grade_avg)
        list2d_gradeavg.append(list1d_gradeavg)

    list2d_gradeavg.sort(key = lambda   list1d_gradeavg : list1d_gradeavg[2] )
    print(list2d_gradeavg)

def Main():
    print("------------这是一个简单的学籍管理系统------------\n")
    while 1:
        Check_Flag = Datacheck()
        print('''请输入数字选择功能：1.建立新学籍档案  2.添加新学生的学籍  3.学籍查询
                 4.录入新成绩     5.平均分计算       0.退出程序''')
        choice = int(input())
        if choice == 1:
            if Check_Flag:
                flag_1 = int(input("检测到已有学籍档案，是否覆盖。\n1.覆盖 2.返回"))
                if flag_1 == 1:
                    Grade_input()
                elif flag_1 == 2:
                     continue
                else:
                    print("输入有误，请重新输入")
            else:
                    Grade_input()

        elif choice == 2:
            if Check_Flag:
                info_student = Stu_add()
            else:
                print("------------档案不存在，请先建立档案------------")

        elif choice == 3:
            if Check_Flag:
                info_student = Grade_read()
                index_stu = Stu_seek(info_student)
                global check_stu
                if check_stu:
                    flag_2 = int(input("是否删除该生学籍档案\n 1.删除 2.返回"))
                    if flag_2 == 1:
                        Stu_del(info_student,index_stu)
                        Savechange(info_student)
            else:
                print("------------档案不存在，请先建立档案------------")


        elif choice == 4:
            if Check_Flag:
                info_student = Grade_read()
                Newgrade_add(info_student)
                Savechange(info_student)
            else:
                print("------------档案不存在，请先建立档案------------")

        elif choice == 5:
            if Check_Flag:
                info_student = Grade_read()
                Grade_avg(info_student)
            else:
                print("------------档案不存在，请先建立档案------------")

        elif choice == 0:
            break

        else:
            print("请重新输入")

    print("test end")

Main()