#coding time:13.Feb
''' 构造一个简单的swtich函数。

def Switch(Var):
    return  {'a':1, 'b':2, 'c':3 }.get(Var,0)
利用字典的特性与.get函数 得到不同情况的返回值，实现C中的swtich功能。

int Func_Switch(char Var){
    switch(Var){
        case 'a':
            return 1;
        case 'b':
            return 2;
        case 'c':
            return 3;
        default:
            return 0;
    }
}
C中的类比写法。果然高级语言各种意义上都很高级。
'''


#利用Switch功能完成一个简单的选择型计算器功能
#单独写出运算函数，强调字典中的Value可以是函数 <- 重点
#字典中的KEY不能改变，而Value可以是变量（可Hash化的变量都可以？待考证）

def Sum(var_1,var_2):
    return var_1 + var_2

def Subtraction(var_1,var_2):
    return var_1 - var_2

def Multiplication(var_1,var_2):
    return var_1 * var_2

def Division(var_1,var_2):
    return var_1 / var_2

def Str_Split(str):
    #将输入的字符串切割，返回运算符和用户输入的数字
    #若没有对应的运算符则返回False，也可以抛出异常。
    list = ['+','-','*','/']
    for i in range(0,4):
        if list[i] in str:
            Var_list = str.split(list[i])
            return [list[i],float(Var_list[0]),float(Var_list[1])]
    return False

def Switch(key,var_1,var_2):
    return {'+':Sum(var_1,var_2),
            '-':Subtraction(var_1,var_2),
            '*':Multiplication(var_1,var_2,),
            '/':Division(var_1,var_2)}.get(key,0)

def Main():
    str = input("请输入一个简单算式:")
    Expression = Str_Split(str)
    if Expression:
        result = Switch(Expression[0],Expression[1],Expression[2])
        print("=",result)
    else:
        print("输入有误")

Main()

#input:59/5
#print(=11.8)
#过年真的好麻烦，害怕 ><