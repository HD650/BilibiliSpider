# 使用梯度下降法求线性回归，这里提供批量梯度下降法BGD，未来提供随机梯度下降发SGD
import numpy

# Locally weighted least squares revisited
def lwlr(testPoint, xArr, yArr, k=1.0):
    """局部加权线性回归方法，摘自 www.manning.com/MachineLearninginAction
    这种算法优于梯度下降发的地方在于对于局部线性的数据拟合更好,对于视频信息，不同热度区间的视频确实符合不同的线性模型
    该算法的主要参数是k，小k会导致真正进行训练的样本点过少，而k过大则会有大量远距离的样本点影响局部的线性关系"""
    xMat = numpy.matrix(xArr)
    yMat = numpy.matrix(yArr).T
    # 获得样本的数量
    m = xMat.shape[0]
    weights = numpy.matrix(numpy.eye(m))
    for j in range(m):
        diff_mat = testPoint - xMat[j, :]
        weights[j, j] = numpy.exp(diff_mat*diff_mat.T/(-2.0*k**2))
    temp = xMat.T * (weights * xMat)
    if numpy.linalg.det(temp) == 0.0:
        print("矩阵不可逆！")
        return
    ws = temp.I * (xMat.T * (weights * yMat))
    return ws


def bgd(theta, sample_x, sample_y, max_count=999999, alpha=0.05):
    """思路来源于： http://m.blog.csdn.net/article/details?id=51554910
    这里支持变长的theta参数，不支持收敛条件"""
    samples = len(sample_x)
    theta_num = len(theta)
    count = 0
    last = 0
    # 进行一次迭代
    while True:
        count += 1
        for i in range(samples):
            diff = 0
            # 使用sample和theta计算出因变量
            for one in range(theta_num):
                diff += theta[one] * sample_x[i][one]
            # 计算出中间值
            diff -= sample_y[i]
            # 修正所有theta
            for one in range(theta_num):
                theta[one] -= alpha * (diff * sample_x[i][one]) / samples

        # 计算cost function的结果
        error = 0
        for i in range(samples):
            temp = 0
            # 使用修正果的theta和样本计算出因变量
            for one in range(theta_num):
                temp += theta[one] * sample_x[i][one]
            # 使用最大似然计算出cost function的值
            try:
                error += (sample_y[i] - temp) ** 2 / 2 / samples
            except OverflowError as over:
                pass
        # 打印本次迭代的结果
        temp = '[{1}] error : {0} '.format(str(error),str(count))
        for one in range(theta_num):
            temp += 'theta{0} : {1} '.format(str(one), str(theta[one]))
        print(temp)

        # 如果两次迭代的cost function值没变，则认为回归已经收敛，打印结果
        if last == error:
            print('reach convergence! iteration finished! count: ', str(count))
            temp = ''
            for one in range(theta_num):
                temp += 'theta{0} : {1} '.format(str(one), str(theta[one]))
            temp += 'error : {0}'.format(str(error))
            print(temp)
            return theta, error, count
        # 没有收敛则储存上一次的误差值
        else:
            last = error

        # 如果迭代达到最大次数，停止迭代
        if count >= max_count:
            print('reach max count! iteration finished! count: ', str(count))
            temp = ''
            for one in range(theta_num):
                temp += 'theta{0} : {1} '.format(str(one), str(theta[one]))
            temp += 'error : {0}'.format(str(error))
            print(temp)
            return theta, error, count


# 测试数据与代码 test data and code
sample_x = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
sample_y = [2, 3, 6, 8, 10]

theta0 = 0
theta1 = 0
theta2 = 0

# 梯度下降法的测试
# if __name__ == '__main__':
#     import matplotlib.pyplot as plt
#     theta, error, count = bgd([0, 0], sample_x, sample_y, 1000000)
#     x_draw = list()
#     for one in sample_x:
#         x_draw.append(one[:-1])
#     x = numpy.matrix(sample_x)
#     y = numpy.array(sample_y)
#     theta = numpy.matrix(theta)
#     predict_y = x*theta.T
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     ax.plot(x_draw, predict_y)
#     ax.scatter(x_draw, y, s=2, c='red')
#     plt.show()

# 局部加权回归测试，通过调整k，从1到0.2，可以看到拟合越来越好
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x_draw = list()
    predict_y = list()
    for one in sample_x:
        x_draw.append(one[:-1])
        w = lwlr(one[:-1], sample_x, sample_y, 0.2)
        temp = numpy.matrix(one)*w
        temp = temp.max()
        predict_y.append(temp)
        numpy.matrix.data
    y = numpy.array(sample_y)
    predict_y = numpy.array(predict_y)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x_draw, predict_y)
    ax.scatter(x_draw, y, s=2, c='red')
    plt.show()