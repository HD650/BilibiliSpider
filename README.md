# BilibiliSpider- ( ○’ω’○)つロ
This project is used to crawl video information from bilibili damaku site such as amount of plays, favorites, coins and so on. 
This project is developed base on the [scrapy-redis](https://github.com/rolando/scrapy-redis), a  distributed spider framework.  So you have to install redis database and scrapy before you run this project.
## Progress ##
Basically, this project can run. ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄
## Need to fix ##
Correctly run with only one master database, multi-nodes database hasn't been tested yet.
Still have problems to crawl bangumi category videos in bangumi.bilibili.com.
Crawling sometimes stuck with unknown reason. (╯‵□′)╯︵┻━┻  
Redis binaries and configuration files haven't been uploaded.
Will add some code to analyse the data we crawled. 

# B站爬虫- ( ○’ω’○)つロ
这个工程用于从bilibili弹幕网站爬取各个视频的信息，比如播放数，收藏数和硬币数。
这个工程基于[scrapy-redis](https://github.com/rolando/scrapy-redis)分布式爬虫框架开发，所以在使用这个工程之前需要先安装redis分布式数据库和scrapy框架。
## 进度 ##
该工程目前基本可以运行。⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄
## 需要修正 ##
单节点数据库可以运行，多节点数据库还没有测试过。
番剧分类还不能正常爬取。
爬取有时会因为未知原因假死。 (╯‵□′)╯︵┻━┻  
Redis的二进制文件和配置文件还没有上传。
加入一些代码以分析爬取得到的数据。



