#coding time: 18.Feb
#给出一个无向图，实现Dijkstra算法
#具体的路径输出还没写，之后补上
#路径输入已补上 - 18.Feb
'''
eg.无向图
           【1】
      p=5 /    ╲ p=5
        /        ╲
      【0】———p=7——【2】
           ╲       ︱ p=1
             p=3╲  ︱
      【4】———p=2——【3】
'''
class UndirectedGraph:

    def __init__(self,pn,en):
        self.point_num = pn
        self.edge_num = en
        self.arc_matrix = [ [float("inf")] * pn for i in  range(0,pn) ]
        #初始化邻接矩阵。float("inf") = +∞

    def arc_matrix_update(self):
        edge = []
        for i in range(0,self.edge_num):
            str_input = input("输入第"+ str(i+1) + "条边的信息。" + \
            "依次输入第一个端点编号、第二个端点编号、权值(端点编号从0开始、以空格间隔)：")
            edge.append(str_input.split(' '))
            self.arc_matrix[ int(edge[i][0]) ][ int(edge[i][1]) ] = float(edge[i][2])
            self.arc_matrix[ int(edge[i][1]) ][ int(edge[i][0]) ] = float(edge[i][2])
            #无向图，邻接矩阵转置对称： M^T = M。若为有向图则可删去上一行
        return self.arc_matrix

    def Dijkstra(self):
        s_flag = [0] * self.point_num
        # 初始化S集合为空集
        s_flag[0] = 1
        #将起始点：0号点加入集合S
        distance = self.arc_matrix[0]
        # distance储存起始点到其余各点的距离。
        # 可改变[]中的值选择不同的起始点。
        path = ["V0"] * self.point_num
        #利用path列表储存路径信息。
        while(s_flag.count(0)):
            dist_min = float("inf")
            for i in range(self.point_num):
                if ( s_flag[i] == 0 and distance[i] < dist_min ):
                    index = i
            #index为非S集中距离起始点最短的端点编号
            s_flag[index] = 1
            #将该点加入至S集合中
            path[index] += "->V" + str(index)
            #加入S集合意味着从起点到达该点路径已结束，路径写入。
            for i in range(self.point_num):
                if (s_flag[i] == 0 and self.arc_matrix[i][index] + distance[index] <= distance[i]):
                    distance[i] = self.arc_matrix[i][index] + distance[index]
                    # 遍历非S中的点，在加入新点至S后，若距离变短，则改写其到起始点的距离
                    path[i] += "->V" + str(index)
                    # 向path列表中写入中间点路径。
        return distance , path


graph = UndirectedGraph(5,6)
Arc_matrix = graph.arc_matrix_update()
print("邻接矩阵为：" + str(Arc_matrix))
Distance , Path = graph.Dijkstra()
print("从0号点出发，到各点的最短距离为：" + str(Distance))
print("从0号点出发，到各点的最短路径为：" + str(Path))

#print(邻接矩阵为：[[inf, 5.0, 7.0, 3.0, inf],
#                 [5.0, inf, 5.0, inf, inf],
#                  [7.0, 5.0, inf, 1.0, inf],
#                   [3.0, inf, 1.0, inf, 2.0],
#                    [inf, inf, inf, 2.0, inf]])
#print(从0号点出发，到各点的最短距离为：[inf, 5.0, 4.0, 3.0, 5.0])
#print(从0号点出发，到各点的最短路径为：['V0', 'V0->V1', 'V0->V3->V2', 'V0->V3', 'V0->V3->V4'])