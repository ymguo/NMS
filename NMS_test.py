'''

According to what we are discussing about NMS,
please write your own code for NMS in C++ or Python.

For Python, please finish the function:
def NMS(lists, thre):
    # lists is a list. lists[0:4]: x1, x2, y1, y2; lists[4]: score

'''

import numpy as np


def myNMS(lists, thre):

    result_idx = []  # 初始化索引值集合

    x1 = lists[:, 0]
    y1 = lists[:, 1]
    x2 = lists[:, 2]
    y2 = lists[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)  # 计算矩形面积

    scores = lists[:, 4]
    '''
    
    argsort() 函数返回的是数组值从小到大的索引值
    example:
    >>> x = np.array([3, 1, 2])
    >>> np.argsort(x)
    array([1, 2, 0])
    
    '''
    order = scores.argsort()[::-1]  # 降序排列 返回索引值

    while len(order) > 0:
        idx = order[0]  # 取scores最大值索引
        result_idx.append(idx)  # 加入到要返回的索引值集合

        '''
        
        np.maximum：(X, Y, out=None) 
            X 与 Y 逐位比较取其大者；
            最少接收两个参数
        example:
        >> np.maximum([-2, -1, 0, 1, 2], 0)
        array([0, 0, 0, 1, 2])
            
        '''
        # IOU计算，索引减一
        iou_x1 = np.maximum(x1[idx], x1[order[1:]])
        iou_y1 = np.maximum(y1[idx], y1[order[1:]])

        iou_x2 = np.minimum(x2[idx], x2[order[1:]])
        iou_y2 = np.minimum(y2[idx], y2[order[1:]])  ## why minimum ?

        w = np.maximum(0, iou_x2 - iou_x1 + 1)
        h = np.maximum(0, iou_y2 - iou_y1 + 1)

        iou_area = w * h

        iou = iou_area / (area[idx] + area[order[1:]] - iou_area)  ## ???
        '''
        np.where(condition)
        只有条件 (condition)，则输出满足条件 (即非0) 元素的坐标。
        
        >>> a = np.array([2,4,6,8,10])
        >>> np.where(a > 5)             # 返回索引
        (array([2, 3, 4]),)  
        '''
        idx_iou = np.where(iou < thre)[0]  # 选取要保留的索引值

        idx_order = idx_iou + 1  # 将索引值对应到order内 ## why +1 ?

        order = order[idx_order]

    return result_idx


if __name__ == "__main__":

    thre = 0.1

    lists = np.zeros((10, 5))
    lists[:, 0:4] = np.random.randint(100, size=[10, 4])
    lists[:, 4] = np.random.rand(10)
    '''
    lists = np.zeros((5, 5))

    lists[0][0] = 35
    lists[0][1] = 40
    lists[0][2] = 54
    lists[0][3] = 59
    lists[0][4] = 0.35447849

    lists[1][0] = 59
    lists[1][1] = 88
    lists[1][2] = 58
    lists[1][3] = 1
    lists[1][4] = 0.58816124

    lists[2][0] = 42
    lists[2][1] = 67
    lists[2][2] = 49
    lists[2][3] = 67
    lists[2][4] = 0.55697901

    lists[3][0] = 41
    lists[3][1] = 55
    lists[3][2] = 56
    lists[3][3] = 16
    lists[3][4] = 0.36570904

    lists[4][0] = 3
    lists[4][1] = 10
    lists[4][2] = 11
    lists[4][3] = 9
    lists[4][4] = 0.38477632
    '''

    idx_row = myNMS(lists, thre)

    print(idx_row)
    print(lists[idx_row])
