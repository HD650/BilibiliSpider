# 暂时只是个demo，我们通过线性回归可以判断硬币，收藏，评论，up主关注度这几个自变量和因变量播放数的关系，从而推断视频热度
# 中 play，barrage，favorite和reply的大致比值
import matplotlib.pyplot as plt
from data_analysis.linear_regression import bgd, lwlr_normal, lwlr_array
from data_analysis.data_reader import read_video_info
from data_analysis.plot_generator import draw_plays_favorites_coins_3d

# 对数据进行缩小，防止矩阵运算中数量级过大导致程序崩溃
coins_favorites_divisor = 10
plays_divisor = 100
# 局部权重线性算法使用原版还是队列版
lwlr = lwlr_array


def process_samples(video_info):
    """把数据库中的原始数据规整为两个向量，其中x向量加上常量1对应线性方程中的常数项"""
    sample_x = list()
    sample_y = list()
    category = ''
    for key in video_info:
        category = key
    for item in video_info[category]:
        # 对于数量级进行一定处理，否则数据汇溢出，同时加上常数x0为1
        sample_x.append([item[0]/coins_favorites_divisor, item[1]/coins_favorites_divisor, 1])
        sample_y.append(item[3]/plays_divisor)
    return sample_x, sample_y


def lw_regression(video_info):
    """使用局部权重线性回归，对于同一区间的视频，其大致符合线性模型，使用局部权重线性回归算法优于传统线性回归
    同时在k的选择上，暂时使用0.003，这会导致样本不够多的区间运算工程中出现0矩阵，因为k小核函数的区间就越小，下降也越快，
    导致大量样本点的权重为0或者趋近于零，最后权重矩阵为0，矩阵不可逆出错，解决方法是加大k，或者增加更多样本"""
    # 采用局部权重的线性回归，同时仅仅考虑单一分类下的coins,favorites对plays的影响，低热度视频拟合良好，高热度因为样本
    # 较少，拟合效果不好
    sample_x, sample_y = process_samples(video_info)
    print('need a approximate coins and favorites to predicate')
    print('enter coins:')
    coins = int(input())/coins_favorites_divisor
    print('enter favorites:')
    favorites = int(input())/coins_favorites_divisor
    # 使用coins，favorites，1作为目标点，所有数据作为样本
    result = lwlr([coins, favorites, 1], sample_x, sample_y, k=0.1)
    if result is None:
        # 权重矩阵不可逆，一般是因为其值为0，原因是样本不够或者是k取值太小
        print('not enough samples within these coins and favorites!')
        return
    print('get theta result')
    print(str(result))
    # 计算出播放量
    result = [coins, favorites, 1] * result
    print(str(result[0, 0]*plays_divisor))


def draw_lwlr(video_info):
    sample_x, sample_y = process_samples(video_info)
    ax = draw_plays_favorites_coins_3d(video_info)
    sample_x_ordered = list()
    sample_y_ordered = list()
    for i, item in enumerate(sample_x):
        if len(sample_x_ordered) is 0:
            sample_x_ordered.append(item)
            sample_y_ordered.insert(i, sample_y[i])
        else:
            for sample in sample_x_ordered:
                if sample[0] < item[0]:
                    sample_x_ordered.insert(i, item)
                    sample_y_ordered.insert(i, sample_y[i])
                    break
                elif len(sample_x_ordered) is 1:
                    sample_x_ordered.insert(0, item)
                    sample_y_ordered.insert(0, sample_y[i])
                else:
                    continue
    print('sorting finished!')
    draw_y = list()
    for i, item in enumerate(sample_x_ordered):
        ws = lwlr(item, sample_x, sample_y, k=0.2)
        if ws is None:
            sample_x_ordered.pop(i)
            sample_y_ordered.pop(i)
            print('discard')
            continue
        predict_y = item * ws
        predict_y = predict_y[0, 0]
        print(str(item)+'  '+str(predict_y))
        draw_y.append(predict_y)
    ax.plot(sample_x_ordered[:][0], sample_x_ordered[:][1], draw_y)
    plt.show()


def test_k(video_info):
    """测试使用不同不同k情况下的误差"""
    sample_x, sample_y = process_samples(video_info)
    samples = len(sample_x)
    test_sample_x = list()
    test_sample_y = list()
    # 抽取测试数据，其他点作为训练数据
    for i in range(0, samples-1, 3000):
        test_sample_x.append(sample_x.pop(i))
        test_sample_y.append(sample_y.pop(i))
    for k in (0.003, 0.008, 0.01, 0.10, 0.20):
        print('now k is: '+str(k))
        error = 0
        for i in range(len(test_sample_x)):
            result = lwlr(test_sample_x[i], sample_x, sample_y, k)
            if result is None:
                print('not enough samples with these coins and favorites'.format(str(k)))
                continue
            result = test_sample_x[i]*result
            print('result: {0}  sample: {1}'.format(result[0, 0]*plays_divisor, sample_y[i]*plays_divisor))
            # 计算误差
            error += (result[0, 0]-sample_y[i])/sample_y[i]
        # 某k情况下的总误差
        print('total error: '+str(error/len(test_sample_x)*100))
        print()
        print()


def bgd_regression(video_info):
    # 老旧的梯度下降法，并不能很好的拟合
    # 整理数据为线性格式
    sample_x = list()
    sample_y = list()
    category = ''
    for key in video_info:
        category = key
    video_info = video_info[category]
    if video_info:
        for one in video_info:
            temp = list()
            for i, item in enumerate(one):
                if i < len(one) - 1:
                    # 播放量等数据单位过大，在迭代中会超出python表示范围，我们要归一化
                    temp.append(item/coins_favorites_divisor)
                if i == len(one) - 1:
                    # 播放量等数据单位过大，在迭代中会超出python表示范围，我们要归一化
                    sample_y.append(item/plays_divisor)
            # 我们认为有一个常数项影响
            temp.append(1)
            sample_x.append(temp)
        theta_num = len(sample_x[0])
        # 我们认为有一个常数影响
        theta = [1 for i in range(theta_num)]
        # 送bgd进行迭代
        bgd(theta, sample_x, sample_y, 10000000, 1.0)


if __name__ == '__main__':
    video_info = read_video_info()
    # draw_lwlr(video_info)
    # lw_regression(video_info)
    test_k(video_info)

