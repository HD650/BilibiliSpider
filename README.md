# BilibiliSpider- ( ○’ω’○)つロ
This project is used to crawl video information from bilibili damaku site such as amount of plays, favorites, coins and so on.  
This project is developed base on the [scrapy-redis](https://github.com/rolando/scrapy-redis), a  distributed spider framework.  So you have to install redis database and scrapy before you run this project.  
You (maybe) can deploy this spider and the corresponding redis notes on several machines to speed up the crawling.
## Dependencies ##
Pyhton 3.4  
Ruby 2.x  
scarpy  
scrapy-redis  
redis-py  
redis-py-cluster  
## Progress ##
Basically, this project can run. ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄  
## Problem ##
Still have problems to crawl bangumi category videos in bangumi.bilibili.com.  
Crawling sometimes stuck with unknown reason. (╯‵□′)╯︵┻━┻  
Redis cluster doesn't support transaction, may cause some atomic problem.
## Future ##
Will add some code to analyse the data we crawled.  
Correctly run one spider with cluster database deployed on the same machine，running with database and spiders deployed on different machines haven't been tested yet.  
Distribute the keys of items in a more flat manner, so the payload is distributed to different redis notes.  
One script to start the whole project easily.
  

# B站爬虫- ( ○’ω’○)つロ
这个工程用于从bilibili弹幕网站爬取各个视频的信息，比如播放数，收藏数和硬币数。  
这个工程基于[scrapy-redis](https://github.com/rolando/scrapy-redis)分布式爬虫框架开发，所以在使用这个工程之前需要先安装redis分布式数据库和scrapy框架。 
你可以将该爬虫和对应的redis节点部署在不同机器上以提高爬取的速度。
## 环境需求 ##
Pyhton 3.4  
Ruby 2.x  
scarpy  
scrapy-redis  
redis-py  
redis-py-cluster   
## 进度 ##
该工程目前基本可以运行。⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄  
## 问题 ## 
番剧分类还不能正常爬取。 
爬取有时会因为未知原因假死。 (╯‵□′)╯︵┻━┻   
Redis集群不支持事物，会造成一些原子性问题。
## 未来计划 ##
加入一些代码以分析爬取得到的数据。 
单机器上的单爬虫进程和redis集群可以正常运行，多机器的集群还没有测试。
把item的key分散到redis的hash空间去，这样可以把数据库的负载分散。  
通过一个脚本运行全部的工程。



