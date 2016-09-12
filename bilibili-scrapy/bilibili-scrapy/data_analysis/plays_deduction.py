# 暂时只是个demo，我们通过线性回归可以判断硬币，收藏，评论，up主关注度这几个自变量和因变量播放数的关系，从而推断up的视频
# 播放量是否正常（我们假设这几个数据之间是线性关系）
# from now, this is a demo, we can deduce the number of plays from the information of coins, favorites and replys
# (now, we assume these features fit in a linear regression)

from data_analysis.linear_regression import bgd
from data_analysis.process_items import get_cursor
import sys
sys.path.append(r'.\bilibili-scrapy')
sys.path.append(r'..')
import settings

if __name__ == '__main__':
    database = settings.SQL_DATABASE
    table = settings.SQL_TABLE
    cur, conn = get_cursor()
    # 取出所有分类，我们认为分类会影响播放量
    category_query = '''SELECT category FROM {0} GROUP BY category ORDER BY category;'''.format(table)
    cur.execute(category_query)
    categories = cur.fetchall()
    print('Please choose one category:')
    for i, categorie in enumerate(categories):
        print(str(i)+' : '+str(categorie))
    i = int(input())
    categorie = categories[i][0]
    print(str(categorie)+' is selected!')
    # 取出所有的视频信息，其中弹幕数，硬币数，收藏数和回复数作为features，播放数作为target(分类应该提前分好)
    videoinfo_query = '''SELECT barrages,coins,favorites,replys,plays
                          FROM {0} WHERE category='{1}';'''.format(table, categorie)
    cur.execute(videoinfo_query)
    video_info = cur.fetchall()
    print(str(len(video_info))+' samples are found!')
    # 播放量是所有数据中单位最大的，我们使用最大播放量来把所有数据归一化
    max_query = '''SELECT plays FROM {0} WHERE category='{1}' ORDER BY plays DESC LIMIT 0,1;'''.format(table, categorie)
    cur.execute(max_query)
    # 所有数据归一化为0~100的值，防止迭代中出现无穷
    max_plays = cur.fetchone()[0]/100
    print('normalized by '+str(max_plays))
    sample_x = list()
    sample_y = list()

    # 整理数据为线性格式，其中每一种分类视为一个feature
    if video_info:
        for one in video_info:
            temp = list()
            for i, item in enumerate(one):
                if i < len(one) - 1:
                    # 播放量等数据单位过大，在迭代中会超出python表示范围，我们要归一化
                    temp.append(item/max_plays)
                if i == len(one) - 1:
                    # 播放量等数据单位过大，在迭代中会超出python表示范围，我们要归一化
                    sample_y.append(item/max_plays)
            # 我们认为有一个常数项影响
            temp.append(1)
            sample_x.append(temp)
        theta_num = len(sample_x[0])
        # 我们认为有一个常数影响
        theta = [1 for i in range(theta_num)]
        # 送bgd进行迭代
        bgd(theta, sample_x, sample_y, 10000000, 1.0)
