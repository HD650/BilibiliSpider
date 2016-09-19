from  data_analysis.process_items import get_cursor
import settings


def read_video_info():
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
                videoinfo_query = '''SELECT coins,favorites,barrages,plays,name,av,replys
                                          FROM {0} WHERE category='{1}';'''.format(table, str(categories[int(one)][0]))
                cur.execute(videoinfo_query)
                video_info[categories[int(one)][0]] = cur.fetchall()
            print(str(len(video_info))+' categories are selected!')
            return video_info
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
                return temp
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
                return video_info
    finally:
        cur.close()
        conn.close()