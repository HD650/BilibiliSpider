# 暂时只是个demo，我们通过线性回归可以判断硬币，收藏，评论，up主关注度这几个自变量和因变量播放数的关系，从而推断视频热度
# 中 play，barrage，favorite和reply的大致比值

from data_analysis.linear_regression import bgd, lwlr
from data_analysis.data_reader import read_video_info
from data_analysis.plot_generator import draw_plays_favorites_coins_3d
import sys
sys.path.append(r'.\bilibili-scrapy')
sys.path.append(r'..')
import settings

if __name__ == '__main__':
    video_info = read_video_info()
    sample_x = list()
    sample_y = list()

    # 老旧的梯度下降法，并不能很好的拟合
    # # 整理数据为线性格式
    # if video_info:
    #     for one in video_info:
    #         temp = list()
    #         for i, item in enumerate(one):
    #             if i < len(one) - 1:
    #                 # 播放量等数据单位过大，在迭代中会超出python表示范围，我们要归一化
    #                 temp.append(item/max_plays)
    #             if i == len(one) - 1:
    #                 # 播放量等数据单位过大，在迭代中会超出python表示范围，我们要归一化
    #                 sample_y.append(item/max_plays)
    #         # 我们认为有一个常数项影响
    #         temp.append(1)
    #         sample_x.append(temp)
    #     theta_num = len(sample_x[0])
    #     # 我们认为有一个常数影响
    #     theta = [1 for i in range(theta_num)]
    #     # 送bgd进行迭代
    #     bgd(theta, sample_x, sample_y, 10000000, 1.0)

    # 采用局部权重的线性回归，同时仅仅考虑单一分类下的coins,favorites对plays的影响，拟合效果良好
    category = ''
    for key in video_info:
        category = key
    for item in video_info[category]:
        sample_x.append([item[1]/100, item[2]/100])
        sample_y.append(item[3]/10000)
    print('need a approximate coins and favorites to predicate')
    print('enter coins:')
    coins = int(input())
    print('enter favorites:')
    favorites = int(input())
    result = lwlr([coins, favorites], sample_x, sample_y, k=0.1)
    print('get theta result')
    print(str(result))
    result = [coins, favorites] * result
    print(str(result))
