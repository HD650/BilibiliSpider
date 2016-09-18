# 使用jieba分词库，总体认为其default分词效果最好，还需要我们增加一些up主名字，游戏名字等
from data_analysis.process_items import *
import jieba

if __name__ == '__main__':
    jieba.load_userdict('bilibili_dict.txt')
    database = settings.SQL_DATABASE
    table = settings.SQL_TABLE
    cur, conn = get_cursor()
    try:
        query = '''SELECT name FROM video
                    ORDER BY (plays+barrages+coins+favorites) DESC LIMIT 0,1000;'''.format(table)
        cur.execute(query)
        names = cur.fetchall()
        word_set = dict()
        for name in names:
            temp = name[0].lower()
            seg_list = jieba.lcut(temp, cut_all=False)
            print("Default Mode: " + "/ ".join(seg_list))
            for item in seg_list:
                if item in word_set:
                    word_set[item] += 1
                else:
                    word_set[item] = 1
            print()
        for key in word_set:
            print(str(key)+' : '+str(word_set[key]))
    except Exception as e:
        str(e)
    finally:
        cur.close()
        conn.close()