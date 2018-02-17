#coding time:16.Feb
#粗略估计浮点车在一段时间内的里程
#实验数据：X年X月X日1h内某浮点车的GPS轨迹点数据
#原始txt数据采取utf-16le编码，按时间顺序排列。
#1h内GPS轨迹点数共计309个，轨迹点时间分布较为均匀，平均约11s得到一个轨迹点数据。
#思路：将数据内的经纬度信息利用高斯-克吕格投影转换为对应带号的大地平面坐标。
#根据11s内大地平面坐标的变化，利用D=((dx)^2+(dy)^2)^(1/2)粗略估计浮点车的位移，并将位移累加。
#精度：基本不用考虑精度，很差很差。记计算得到的里程为D，实际为D0。
#1：假设11s内浮点车转弯，D < D0
#2：假设11s内浮点车调头，D < D0
#3：道路并非严格直线，D < D0
#4：GPS残差，无法避免。
#改进思路：获取道路路网矢量图，利用点的位移变化推测浮点车可能的路线，利用路网辅助完成里程统计。

import math
import codecs
global Pi, a, b, f, e , e_2, L_0, p, m0, m2, m4, m6, m8, a0, a2, a4, a6, a8

Pi = 3.1415926
a = 6378137.0
b = 6356752.0
f = 1 / 298.2572236
e = (((a ** 2) - (b ** 2)) ** 0.5) / a
e_2 = (((a ** 2) - (b ** 2)) ** 0.5) / b
L_0 = (114.0 * Pi) / 180
# WGS84椭球参数：a、b、f、e 、e_2分别为椭球长半轴、短半轴、扁率、第一偏心率、第二偏心率。
# L_0为3度带中，38号带的中央子午线经度(弧度)

p = (180 / Pi) * 3600
# 与一弧度等价的秒数
m0 = a * (1 - (e ** 2))
m2 = (3 / 2) * (e ** 2) * m0
m4 = 5 * (e ** 2) * m2
m6 = (7 / 6) * (e ** 2) * m4
m8 = (9 / 8) * (e ** 2) * m6
# 基本常量mi(i=0,2,4,6,8)的计算
a0 = m0 + m2 / 2 + (3 / 8) * m4 + (5 / 16) * m6 + (35 / 128) * m8
a2 = m2 / 2 + m4 / 2 + (15 / 32) * m6 + (7 / 16) * m8
a4 = m4 / 8 + (3 / 16) * m6 + (7 / 32) * m8
a6 = m6 / 32 + m8 / 16
a8 = m8 / 128
# 基本常量ai(i=0,2,4,6,8)的计算

def angle_to_rad(x):
    return (x * Pi) / 180

def sin(rad):
    return math.sin(rad)

def cos(rad):
    return math.cos(rad)

def tan(rad):
    return math.tan(rad)

def exp(x,n):
    return float(x ** n)

def BL_to_XY(B,L):
    #将BL坐标(弧度表示）转化为XY坐标(单位:m)，基于WGS-84参考系，采取高斯-克吕格投影算法。
    global Pi, a, b, f, e , e_2, L_0, p, m0, m2, m4, m6, m8, a0, a2, a4, a6, a8
    #声明使用全局变量
    L1 = L - L_0
    #计算与中央子午线的经度差值
    N = ( a * (1 - exp(e,2)) ) / exp( 1 - exp( e * sin(B), 2 ), 1.5 )
    #计算子午圈曲率半径
    yita_exp2 = exp(e_2 * cos(B),2)
    #计算yita的二次方
    X_meridian = a0 * B - sin(B) * cos(B) * \
                 ( (a2 - a4 + a6) + (2 * a4 - (16 / 3) * a6) * exp(sin(B),2) + (16 / 3) * a6 * exp(sin(B),4) )
    #计算子午线长度
    t = exp(tan(B),2)
    #记t为tanB的平方，简化算式
    x = X_meridian + N * sin(B) * cos(B) * exp(L1,2) / ( 2 * exp(p,2) ) + \
        N * sin(B) * exp(cos(B),3) * ( 5 - t + 9 * yita_exp2 + 4 * exp(yita_exp2,2) ) * exp(L1,4) / ( 24 * exp(p,4) ) + \
        N * sin(B) * exp(cos(B),5) * ( 61 - 58 * t + exp(t,2) ) * exp(L1,6) / ( 720 * exp(p,6) )
    y = N * cos(B) * L1 / p + N * exp(cos(B),3) * (1 - t + yita_exp2 ) * exp(L1,3) / (6 * exp(p,3)) + \
        N * exp(cos(B),5) *( 5 - 18 * t + exp(t,2) + 14 * yita_exp2 - 58 * yita_exp2 * exp(t,2) ) * exp(L1,5) / (120 * exp(p,5))
    #搬运公式没啥好注释的。以后的bal不要嫌公式麻烦，我知道你肯定要吐槽的。
    y += 500000
    #避免y产生负值，加上500km
    return x, y
    #等价 return (x,y) 返回的是元组

def data_exchange():
    #读入原始数据，去掉多余的信息，将经纬度转换成38号带的高斯大地坐标，并将简化的数据写入一个新文档中。
    data_input = open("Input.txt",'r',encoding="utf-16le")
    data_output = open("Gps_point_info.txt",'w',encoding="utf-8")
    #原始数据为utf16小头编码，写入新数据时改为utf8节省空间
    point_info_2d = []
    list = []
    #新建一个二维列表临时储存gps点信息
    i = 1
    for line in data_input.readlines():
        point_info_1d = line.split()
        point_info_2d.append(point_info_1d)

    for line in point_info_2d:
        L = angle_to_rad(float(line[3]))
        B = angle_to_rad(float(line[4]))
        x, y = BL_to_XY(B,L)
        data_output.write(str(i)+' '+str(x)+' '+str(y)+'\n')
        #仅保存点号、经度、纬度 信息。（时间已经是顺序排列，故舍去）
        i += 1
    data_input.close()
    data_output.close()

def point_read():
    point_info = open("Gps_point_info.txt", 'r', encoding="utf-8")
    point_info_2d = []
    #新建一个二维列表临时储存gps点信息
    for line in point_info.readlines():
        point_info_1d = line.split()
        point_info_2d.append(point_info_1d)
    point_info.close()
    return point_info_2d

def distance_calculate(info_2d):
    # 计算浮点车一段时间内的总里程，实验数据为1h内浮点车的运行点迹
    distance_sum = 0.0
    for index in range(0,len(info_2d)):
        dx = float(info_2d[index][1]) - float(info_2d[index + 1][1])
        dy = float(info_2d[index][2]) - float(info_2d[index + 1][2])
        distance_sum += exp(exp(dx,2)+exp(dy,2),0.5)
        if index + 2 == len(info_2d):
            break
    return distance_sum

def Main():
    data_exchange()
    #数据改写成大地平面坐标形式
    point_info_2d = point_read()
    #得到轨迹点数据的二维列表
    Distance=distance_calculate(point_info_2d)
    #计算浮点车一段时间内的总里程
    print("1h内总里程为：" + str(Distance) + 'm')


Main()
#print(1h内总里程为：31461.0422633379m)