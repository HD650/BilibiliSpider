# 使用梯度下降法求线性回归，这里提供批量梯度下降法BGD，未来提供随机梯度下降发SGD

# 测试数据与代码 test data and code
# sample_x = [(1, 0., 3), (1, 1., 3), (1, 2., 3), (1, 3., 2), (1, 4., 4)]
# sample_y = [95.364, 97.217205, 75.195834, 60.105519, 49.342380]
#
# theta0 = 0
# theta1 = 0
# theta2 = 0
# if __name__ == '__main__':
#     bgd([0, 0, 0], sample_x, sample_y, 1000000)


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


