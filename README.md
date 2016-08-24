# BilibiliSpider- ( ○’ω’○)つロ
This project is used to crawl video information from [bilibili](http://www.bilibili.com/) damaku site such as amount of plays, favorites, coins and so on.     
This project is developed base on the [scrapy-redis](https://github.com/rolando/scrapy-redis), a  distributed spider framework.  So you have to install [redis](http://redis.io/) database and [scrapy](https://github.com/scrapy/scrapy) before you run this project.   
You can deploy this spider and the corresponding redis notes on several machines to speed up the crawling (maybe).
## Dependencies ##
Pyhton 3.4  
Ruby 2.x  
scarpy  
scrapy-redis  
redis-py  
redis-py-cluster  
## Progress ##
Basically, this project can run. ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄  
## Changes##

 - 8.24

Bilibili changed its logic in index page, so our spider should be modified too.   
Sloved the import problem when spider running through terminal.   
Tested the multi-spider crawling and it performed well.    

 - 8.18

Now support redis cluster to speed up the crawling and extend the memory.   
Every urlopen have its timeup now, so the spiders will not stuck anymore.   

 - 8.16

Items we crawled will be temporarily saved in redis database.   
Redis binaries updated.   

 - 8.15

Fundamental code updated.   
## Problem(╯‵□′)╯︵┻━┻ ##
Still have problems to crawl bangumi category videos in bangumi.bilibili.com.     
Redis cluster doesn't support transaction, may cause some atomic problem.   
## Future ##
Will add some code to analyse the data we crawled.  
Correctly run multi-spiders with cluster database deployed on the same machine，running with database and spiders deployed on different machines haven't been tested yet.  
Distribute the keys of items in a more flat manner, so the payload is distributed to different redis notes.  
Analyse the age and gender of users who reply the popular videos.
One script to start the whole project easily.   
Deploy a webserver to show all the data and analysis result.
  

# B站爬虫- ( ○’ω’○)つロ
这个工程用于从[bilibili](http://www.bilibili.com/)弹幕网站爬取各个视频的信息，比如播放数，收藏数和硬币数。   
这个工程基于[scrapy-redis](https://github.com/rolando/scrapy-redis)分布式爬虫框架开发，所以在使用这个工程之前需要先安装[redis](http://redis.io/)分布式数据库和[scrapy](https://github.com/scrapy/scrapy)框架。   
你可以将该爬虫和对应的redis节点部署在不同机器上以提高爬取的速度（大概吧）。
## 环境需求 ##
Pyhton 3.4  
Ruby 2.x  
scarpy  
scrapy-redis  
redis-py  
redis-py-cluster   
## 进度 ##
该工程目前基本可以运行。⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄  
## 更改 ##

 - 8.24

Bilibili 改变了目录页面的逻辑，所以我们的爬虫代码也要改变。   
从控制台启动爬虫时出现的import问题已经解决。   
测试了多爬虫连接redis集群的情况，运行没有问题。    

 - 8.18

现在支持连接redis数据库集群，这样可以加速爬取，并且扩大可用内存。  
所有对urlopen的调用都有了时间限制，现在爬虫不会突然假死了。   

 - 8.16

爬取到的item现在都会被暂时存储在redis中。   
redis的二进制执行文件已经上传。   

 - 8.15

基础代码上传。   
## 问题(╯‵□′)╯︵┻━┻ ## 
番剧分类还不能正常爬取。       
Redis集群不支持事物，会造成一些原子性问题。
## 未来计划 ##
加入一些代码以分析爬取得到的数据。  
单机器上的多爬虫进程和redis集群可以正常运行，多机器的集群还没有测试。  
把item的key分散到redis的hash空间去，这样可以把数据库的负载分散。   
对于高播放视频，分析其回复用户的注册年龄和性别。   
通过一个脚本运行全部的工程。  
部署一个web服务来展示数据和分析结果。  
