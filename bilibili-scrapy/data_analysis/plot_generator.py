# -*- coding: utf-8 -*-
from pylab import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d, Axes3D
import random
import numpy as np
from data_analysis.process_items import get_cursor
import sys
sys.path.append(r'.\bilibili-scrapy')
sys.path.append(r'..')
import settings
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


def draw_categories_3d(video_info):
    '''通过sql数据库的数据画出视频信息图'''
    # 初始化画板
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 遍历得出个指标最大视频
    max = dict()
    plays_max = 0
    favorites_max = 0
    barrages_max = 0
    coins_max = 0
    max['plays_max_index'] = ['', 0]
    max['favorites_max_index'] = ['', 0]
    max['barrages_max_index'] = ['', 0]
    max['coins_max_index'] = ['', 0]
    for key in video_info:
        for index, item in enumerate(video_info[key]):
            if plays_max < item[3]:
                plays_max = item[3]
                max['plays_max_index'][0] = key
                max['plays_max_index'][1] = index
            if favorites_max < item[1]:
                favorites_max = item[1]
                max['favorites_max_index'][0] = key
                max['favorites_max_index'][1] = index
            if barrages_max < item[2]:
                barrages_max = item[2]
                max['barrages_max_index'][0] = key
                max['barrages_max_index'][1] = index
            if coins_max < item[0]:
                coins_max = item[0]
                max['coins_max_index'][0] = key
                max['coins_max_index'][1] = index

    # 为每个视频画点，x为coins，y为favorites，z为barrages，大小代表plays
    for key in video_info:
        coins = list()
        favorites = list()
        plays = list()
        barrages = list()
        for item in video_info[key]:
            coins.append(item[0])
            favorites.append(item[1])
            plays.append(item[3])
            barrages.append(item[2])
        plays = np.array(plays)
        plays = plays/plays_max*300
        ax.scatter(coins, favorites, barrages, marker='o', s=plays,
                   label=key, c=(random.random(), random.random(), random.random()), depthshade=False)

    # 标注出指标最大视频
    for key in max:
        ax.text(video_info[max[key][0]][max[key][1]][0],
                video_info[max[key][0]][max[key][1]][1],
                video_info[max[key][0]][max[key][1]][2],
                video_info[max[key][0]][max[key][1]][4],
                size=10, zorder=1, color='k')

    # 添加label和legend等
    ax.set_xlabel('硬币')
    ax.set_ylabel('收藏')
    ax.set_zlabel('弹幕')
    ax.set_xlim(0)
    ax.set_ylim(0)
    ax.set_zlim(0)
    plt.legend()
    plt.title('视频3d图')
    plt.suptitle('大小代表播放量')
    plt.show()


if __name__ == '__main__':
    database = settings.SQL_DATABASE
    table = settings.SQL_TABLE
    cur, conn = get_cursor()
    # 取出所有分类
    category_query = '''SELECT category,count(1) FROM {0} GROUP BY category ORDER BY category;'''.format(table)
    cur.execute(category_query)
    categories = cur.fetchall()
    print('Please choose one category:')
    for i, category in enumerate(categories):
        print(str(i)+' : '+str(category[0])+' , '+str(category[1]))
    i = input()
    try:
        # 多输入则一次查询各个分类
        if i.find(',') is not -1:
            i = i.split(',')
            video_info = dict()
            print('loading...')
            for one in i:
                videoinfo_query = '''SELECT coins,favorites,barrages,plays,name
                                          FROM {0} WHERE category='{1}';'''.format(table, str(categories[int(one)][0]))
                cur.execute(videoinfo_query)
                video_info[categories[int(one)][0]] = cur.fetchall()
            print(str(len(video_info))+' categories are selected!')
            draw_categories_3d(video_info)
        else:
            # 但输入查询一个分类
            i = int(i)
            if i < len(categories):
                category = categories[i][0]
                print(str(category)+' is selected!')
                # 取出所有的视频信息
                print('loading...')
                videoinfo_query = '''SELECT coins,favorites,barrages,plays,name
                                      FROM {0} WHERE category='{1}';'''.format(table, category)
                cur.execute(videoinfo_query)
                video_info = cur.fetchall()
                print(str(len(video_info))+' samples are found!')
                temp = dict()
                temp[category] = video_info
                draw_categories_3d(temp)
            # 查询所有分类
            else:
                print('no category selected!')
                video_info = dict()
                print('loading...')
                for category in categories:
                    videoinfo_query = '''SELECT coins,favorites,barrages,plays,name
                                          FROM {0} WHERE category='{1}';'''.format(table, str(category[0]))
                    cur.execute(videoinfo_query)
                    video_info[category] = cur.fetchall()
                print(str(len(video_info))+' categories are selected!')
                draw_categories_3d(video_info)
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()