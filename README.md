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

 - 9.3

Started to manage the pages require login, haven't finished yet.        
Started to implement a pipeline insert items directly to SQL database. (Performance of this pipeline still need to be tested)    

 - 9.2

Now item_process.py can transfer all items in redis to SQL database which configured in settings.py.        
Fix some format problems in datetime.   

 - 8.31

Make the distribution of item keys more flat so they can cover all the nodes in cluster.   
Now the process_item.py can iterate all items in redis(iterating will delete the item). Soon, it can transfer the item to SQL database.    
Added some batch files to start the cluster(3 instances) and spiders(5 instances) more conveniently and fast.   

 - 8.29

Tested the muti-spider crawling and redis cluster in different machines, didn't find errors from now.    

 - 8.26

Clear the old dirty data in redis.   
Slove some problems occured when using different version of scrapy-redis with author.   
The spider now support both cluster and  single node mode of redis, you can config it in setting.py.   

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
Didn't test wether access to redis cluster faster than directly access to SQL database. (Some books and documents recommend to use redis but i haven't test this case yet)     
Some page need login(the other way, cookies), but sending cookies require more work and bandwidth. Considering temporarily store all these pages and crawl them later.   
Now, spiders can't update video data in redis since the dupefilter stops them to crawl the pages they have seen before.    
## Future ##
Will add some code to analyse the data we crawled.  
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

 - 9.3

开始处理需要登录的页面，暂时还不能处理。        
开始实现一个直接把数据存入sql的管道。 (并不知道这样的性能如何)     

 - 9.2

现在可以使用item_process.py来把所有item转存到SQL数据库中，SQL数据库在settings文件内配置。         
修复了一些日期格式问题。   

 - 8.31

使item的key均匀的分布在redis的空间中，使负载分散在集群的各个节点内。   
现在process_item.py可以迭代出redis中的所有item，不久后他就能把item都转存在sql数据库内。   
增加了能快速方便启动集群(3个实例)和爬虫(5个实例)的批处理文件。      

 - 8.29

测试了多机器下的多爬虫和redis集群运行，目前没有发现问题。  
 - 8.26

删除了redis中的旧数据。    
解决了和作者使用不同版本scrapy-redis时出现的版本问题。    
爬虫下现在同时支持集群redis和单节点redis，你可以在setting.py中配置。     

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
## 问题(╯‵□′)╯︵┻━┻ 
番剧分类还不能正常爬取。       
Redis集群不支持事物，会造成一些原子性问题。  
还未测试连接redis集群是否真的快于连接SQL数据库。(一些数据和文档推荐使用redis最为数据库，但是我还没有测试哪个更快)     
有些页面需要登录才能访问（需要cookies），但是发送cookies需要额外的代码和带宽。暂时考虑把这些网页暂存起来之后统一爬取。  
现在爬虫不能更新redis中的数据，因为dupefilter会阻止爬虫爬取之前见过的页面。    
## 未来计划 ##
加入一些代码以分析爬取得到的数据。       
对于高播放视频，分析其回复用户的注册年龄和性别。   
通过一个脚本运行全部的工程。  
部署一个web服务来展示数据和分析结果。  
