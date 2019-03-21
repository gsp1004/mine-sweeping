# 扫雷程序
"""
# 作者：gsp
# 时间：2019年3月21日 07:20:11
# 许可证：没有，如果你们看得上，随便用
思路：
1.根据游戏的行和列生成width * height 的全0矩阵/二维数组
2.根据雷的个数随机生成地雷
3.生成地雷周围的数字
4.排雷算法，空白则打开周围8格
"""

from random import randint
from os import system

# 函数功能：生成地雷
# 参数一：地雷矩阵行数
# 参数二：地雷矩阵列数
# 参数三：要生成的地雷个数
# 返回值：保存着地雷坐标的列表，地雷坐标为元组
def random_mine(width, height, mine_num):
    ret = []
    for i in range(mine_num):
        while True:
            mine = (randint(0, width-1), randint(0, height-1))
            if mine not in ret:
                ret.append(mine)
                break
    return ret


# 生成地雷周围的数字
# 参数一：地雷矩阵行数
# 参数二：地雷矩阵列数
# 参数三：地雷列表
# 返回值：包含地雷周围数字的二维列表
def generate_num_around_mine(width, height, mine):
    interface = [[0 for i in range(height)] for i in range(width)]  # width * height 的全0矩阵/二维数组
    for i in mine:
        if 0 < i[0] < (width-1) and 0 < i[1] < (height-1):  # 中心
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    interface[i[0] + x][i[1] + y] += 1
        elif i[0] == 0 and 0 < i[1] < (height-1):  # 中上
            for x in [0, 1]:
                for y in [-1, 0, 1]:
                    interface[i[0] + x][i[1] + y] += 1
        elif i[0] == (width-1) and 0 < i[1] < (height-1):  # 中下
            for x in [-1, 0]:
                for y in [-1, 0, 1]:
                    interface[i[0] + x][i[1] + y] += 1
        elif 0 < i[0] < (width-1) and (i[1] == 0):  # 中左
            for x in [-1, 0, 1]:
                for y in [0, 1]:
                    interface[i[0] + x][i[1] + y] += 1
        elif 0 < i[0] < (width-1) and (i[1] == (height-1)):  # 中右
            for x in [-1, 0, 1]:
                for y in [-1, 0]:
                    interface[i[0] + x][i[1] + y] += 1

        elif 0 == i[0] and 0 == i[1]:  # 左上
            for x in [0, 1]:
                for y in [0, 1]:
                    interface[i[0] + x][i[1] + y] += 1
        elif (width-1) == i[0] and 0 == i[1]:  # 左下
            for x in [-1, 0]:
                for y in [0, 1]:
                    interface[i[0] + x][i[1] + y] += 1
        elif 0 == i[0] and (height-1) == i[1]:  # 右上
            for x in [0, 1]:
                for y in [-1, 0]:
                    interface[i[0] + x][i[1] + y] += 1
        elif (width-1) == i[0] and (height-1) == i[1]:  # 右下
            for x in [-1, 0]:
                for y in [-1, 0]:
                    interface[i[0] + x][i[1] + y] += 1

    for i in mine:
        interface[i[0]][i[1]] = 9
    return interface


# 排雷过程
# 雷表
# 打开列表
# 要打开的坐标
# 返回值 0 成功打开
#       -1 踩雷
def pailei(interface, isopen, width, height, x_y):
    if not (-1 < x_y[0] < width and -1 < x_y[1] < height):  # 坐标越界，跳过
        return 0
    if isopen[x_y[0]][x_y[1]]:  # 已经打开，直接跳过
        return 0

    x = x_y[0]
    y = x_y[1]
    if interface[x][y] == 9:  # 踩雷
        return -1
    elif interface[x][y] > 0:  # 单个数字打开
        isopen[x][y] = 1
        return 0
    elif interface[x][y] == 0:  # 空白，打开周围8个
        isopen[x][y] = 1
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == 0 and j == 0):
                    pailei(interface, isopen, width, height, (x+i, y+j))
        return 0


def main():
    width = 9  # 行
    height = 9  # 列
    mine_num = 10  # 地雷个数
    # interface = [[0 for i in range(height)] for i in range(width)]  # width * height 的全0矩阵/二维数组
    mine = random_mine(width, height, mine_num)  # 地雷坐标的列表
    interface = generate_num_around_mine(width, height, mine)
    is_open = [[0 for i in range(height)] for i in range(width)]  # 是否开了

    for i in interface:
        """print(i)
        """
        for j in i:
            print(j, end="  ")
        print("")

    while True:
        while True:
            zuobiao = input("要排的雷坐标，空格隔开:")
            x_y = []
            for i in zuobiao.split(" "):
                if not i.isspace():
                    if i.isnumeric():
                        x_y.append(int(i))
            if len(x_y) != 2:
                system("cls")
                print("输入的不是2个数，重来！")
                continue
            else:
                if is_open[x_y[0]][x_y[1]]:
                    print("这个已经打开了，干嘛么大兄弟！！再来")
                    continue
                elif not (-1<x_y[0]<width and -1<x_y[1]<height):
                    print("超出边界，重来！")
                    continue
                else:
                    break

        if pailei(interface, is_open, width, height, x_y):  # 踩雷了
            print("boom 踩雷啦渣渣~~~~~~")
            break

        count = 0
        for i in range(width):
            for j in range(height):
                if is_open[i][j]:
                    print(interface[i][j], end="  ")
                else:
                    print("*", end="  ")
                    count += 1
            print("")

        if count == mine_num:
            print("厉害了我的哥，恭喜过关")
            break

    print("游戏结束")


if __name__ == '__main__':
    main()
