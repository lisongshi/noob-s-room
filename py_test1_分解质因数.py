#coding time:10.Feb
#输入一个正整数，找到它的质因数
#分为两步：1.找到它的因数 2.判断因数是否是质数
#import random
#之前想试试Python的随机函数，写的random
def Primenum_Check(num):
    #判断num是否为质数,质数:return 1,合数：return 0
    flag = 0
    for i in range(2, int(num/2)+1):
    #range(2,2)不会取值2。
        if num % i == 0:
             flag = 1
             break
    if flag:
        return 0
    else:
        return 1

#num_float = random.random()*100 + 1
#num_int = int(num_float)
#print("生成的随机数为%d\n" %(num_int))
num=int(input("输入一个正整数："))

if num >= 2:
    if Primenum_Check(num):
        print("%d是一个质因数\t" %(num))
        #自身为最大的质因数
    for j in range(2, int(num / 2)+1):
        if num % j == 0:
            if Primenum_Check(j):
                print("%d是一个质因数\t" %(j))
            num /= j

else:
    print("%d没有质因数" %num)
    #其实就是num=1的情况


