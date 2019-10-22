import re
import math
import time
stime = time.time()
i1 = 1
i2 = i3 = i4 = 0  # 标志位
V = M = S = 0  # 分别代表顶点数、三角面片数、边数
point = []  # 顶点索引
face = []  # 面索引
facevector = [0, 0, 0]  # 面的法向量
p1 = re.compile(r'OFF')
p2 = re.compile(r'\d*\s\d*\s\d*')  # 顶点数、三角面片数、边数
p3 = re.compile(r'-?0\.\d+')  # 顶点的三维坐标
p4 = re.compile(r'\d+')  # 依次代表n个顶点、顶点1的索引、 顶点 2 的索引、顶点 3 的索引
file = open('test.off', 'r')
for line in file:
    line.strip('\n')
    lp1 = re.findall(p1, line)
    lp2 = re.findall(p2, line)
    lp3 = re.findall(p3, line)
    lp4 = re.findall(p4, line)
    if i1:
        if lp1:
            i1 = 0
            i2 = 1
            continue
    if i2:
        if lp2:
            lp2 = re.findall(re.compile(r'\d+'), line)
            V = int(lp2[0])
            M = int(lp2[1])
            S = int(lp2[2])
            print(V, M, S)
            i2 = 0
            i3 = 1
            continue
    if i3:
        if lp3:
            for f in range(3):
                lp3[f] = float(lp3[f])
            point.append(lp3)
    if not lp3:
        i3 = 0
        i4 = 1
    if i4:
        lp4.pop(0)
        # print(lp4)
        for f in range(3):
            lp4[f] = int(lp4[f])
        face.append(lp4)
with open('test.stl', 'w') as f:
    f.write('solid Object\n')
for i in range(M):
    a = face[i][0]
    b = face[i][1]
    c = face[i][2]  # a,b,c:面i的三个点的索引
    for j in range(3):  # 面i的法向量
        facevector[j] = point[a][j] / (math.sqrt(math.pow(
            point[a][0], 2) + math.pow(point[a][1], 2) + math.pow(point[a][2], 2)))
    with open('test.stl', 'a') as f:
        f.write('facet normal')
        for j in range(3):
            f.write(' ')
            f.write(str(facevector[j]))
        f.write('\nouterloop\n')
        for j in [a, b, c]:
            f.write('vertex')
            for k in range(3):
                f.write(' ')
                f.write(str(point[j][k]))
            f.write('\n')
        f.write('endloop\nendfacet\n')
        print('已写完第%d条，还剩%d条。' % (i + 1, M - i - 1))
with open('test.stl', 'a') as f:
    f.write('endsolid Object\n')
etime = time.time()
print("程序用时%d分%.2f秒,平均每秒处理%.2f条"%((etime - stime)//60,(etime - stime)%60,M/((etime - stime))))
