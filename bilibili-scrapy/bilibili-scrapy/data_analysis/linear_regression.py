# 暂时只是个demo，我们通过线性回归可以判断硬币，收藏，评论，up主关注度这几个自变量和因变量播放数的关系，从而推断up的视频
# 播放量是否正常（我们假设这几个数据之间是线性关系）
# from now, this is a demo, we can deduce the number of plays from the information of coins, favorites and replys
# (now, we assume these features fit in a linear regression)
sample_x = [(1, 0., 3), (1, 1., 3), (1, 2., 3), (1, 3., 2), (1, 4., 4)]
sample_y = [95.364, 97.217205, 75.195834, 60.105519, 49.342380]

theta0 = 0
theta1 = 0
theta2 = 0


def bgd(theta, sample_x, sample_y, max_count=999999, alpha=0.05):
    samples = len(sample_x)
    theta_num = len(theta)
    count = 0
    last = 0
    while True:
        count += 1
        for i in range(samples):
            diff = 0
            for one in range(theta_num):
                diff += theta[one] * sample_x[i][one]
            diff -= sample_y[i]
            for one in range(theta_num):
                theta[one] -= alpha * (diff * sample_x[i][one]) / samples
        error = 0
        for i in range(samples):
            temp = 0
            for one in range(theta_num):
                temp += theta[one] * sample_x[i][one]
            error += (sample_y[i] - temp) ** 2 / 2 / samples
        temp = ''
        for one in range(theta_num):
            temp += 'theta{0} : {1} '.format(str(one), str(theta[one]))
        temp += 'error : {0}'.format(str(error))
        print(temp)
        if last == error:
            print('reach convergence! iteration finished! count: ', str(count))
            temp = ''
            for one in range(theta_num):
                temp += 'theta{0} : {1} '.format(str(one), str(theta[one]))
            temp += 'error : {0}'.format(str(error))
            print(temp)
            return theta, error, count
        else:
            last = error
        if count >= max_count:
            print('reach max count! iteration finished! count: ', str(count))
            temp = ''
            for one in range(theta_num):
                temp += 'theta{0} : {1} '.format(str(one), str(theta[one]))
            temp += 'error : {0}'.format(str(error))
            print(temp)
            return theta, error, count

if __name__ == '__main__':
    bgd([0, 0, 0], sample_x, sample_y, 10000000000000)
