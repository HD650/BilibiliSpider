# BilibiliSpider- ( ○’ω’○)つロ
This project is used to crawl, represent and analyse video information from [bilibili](http://www.bilibili.com/) damaku site such as amount of plays, favorites, coins and so on.     
## Framework##

 1. The spider of this project is developed base on the
    [scrapy-redis](https://github.com/rolando/scrapy-redis), a 
    distributed spider framework.  So you have to install
    [redis](http://redis.io/) database and
    [scrapy](https://github.com/scrapy/scrapy) before you run this
    project.    You can deploy this spider and the corresponding redis
    notes on several machines to speed up the crawling (maybe).
 2. The representation part of this project is developed base on the
    [matplotlib](https://github.com/matplotlib/matplotlib), a python
    plotting library.   
 3. Some data analysis algorithms and libraries are involved, you can
    see more details
        here：    
        [Gradient
            descent linear regression](http://m.blog.csdn.net/article/details?id=51554910) is used
            to deduce the ratio of plays, coins, favorites and replys. But it seems these features do not fit in a linear function.        
        [Locally weighted linear regression](http://www.cnblogs.com/MrLJC/p/4147697.html) is used to deduce plays of a video with some video samples close to it.    
 4. The tokenizer is developed based on [jieba](https://github.com/fxsjy/jieba), a chinese text segmentation library. And add some special terms used in bilibili.     

## Dependencies ##
Pyhton 3.4  
Ruby 2.x  
scarpy  
scrapy-redis  
redis-py  
redis-py-cluster   
matplotlib   
pymysql   
jieba   
## Progress ##
Basically, this project can run. ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄    
Crawled 900 thousand of video info from game category by 10 instances of spider and 2 days period.
Represented video info with 3d plot which help us to have a better view of the whole samples.      
Deducted the play amount of video by locally weighted regression algorithm trained by samples spider crawled, some results have large error but some work well.    
## Changes##

 - 9.21

Add code to calculate the error of locally weighted regression, so we can choose a best value of k.    
Add constant term which is forgot in previous commits. It helps to decrease the error, but in some cases, the error is still large.           

 - 9.18

Add locally weighted regression algorithm that fit the samples better in a little scale.       
Add sql file which contains some video info samples crawled from game category of bilibili.     

 - 9.18

Add a scirpt to tokenize the name of videos, this will help us to find the most popular words in bilibili.       

 - 9.17

Add a scirpt to represent video information in 3D plot, it has some performance problem. (very slow when drawing thousands of points)    

 - 9.12

Add a script using BGD algorithm to deduct plays of video, it's no accurate yet since we didn't consider the popularities of authors. (lso, these features are not precisely fit in a linear function)         

 - 9.10

Add a gradient descent framework, it will soon trained by data we crawled and to deduct the proportion of plays, coins and favorites.      

 - 9.3 (paused)

Started to manage the pages require login, haven't finished yet.        
Started to implement a pipeline insert items directly to SQL database. (Performance of this pipeline still need to be tested)    

 - 9.2

Now item_process.py can transfer all items in redis to SQL database which configured in settings.py.        
Fix some format problems in datetime.   

 - 8.31

Make the distributions of item keys more flat so they can cover all the nodes in cluster.   
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
Redis cluster sometimes breaks down and can't be fixed up.   
Still have problems to crawl bangumi category videos in bangumi.bilibili.com.     
Redis cluster doesn't support transaction, may causes some atomic problems.   
Didn't test wether accessing to redis cluster faster than directly accessing to SQL database. (Some books and documents recommend to use redis but i haven't test this case yet)     
Some pages need login(the other way, cookies), but sending cookies require more codes and bandwidth. I'm considering temporarily store all these pages and crawl them later.   
Now, spiders can't update video data in redis since the dupefilter stops them to crawl the pages they have seen before.    
Had test a long term crawling but when crawling finished, we didn't go through all pages we want. (only crawled 900000  pages but there were approximate 10000000 pages)    
In some cases, error of locall weighted regression is large, and in some cases, samples are insufficient, maybe we need some kind of non-linear model.    
## Future ##
We need some fileds to record the popularities of authors.   
Will add some code to analyse the data we crawled.  
Analyse the age and gender of users who reply the popular videos.
One script to start the whole project easily.   
Deploy a webserver to show all the data and analysis result.
  

# B站爬虫- ( ○’ω’○)つロ
这个工程用于从[bilibili](http://www.bilibili.com/)弹幕网站爬取、展示和分析各个视频的信息，比如播放数，收藏数和硬币数。   
## 框架 ##

 1. 这个工程的爬虫部分基于[scrapy-redis](https://github.com/rolando/scrapy-redis)分布式爬虫框架开发，所以在使用这个工程之前需要先安装[redis](http://redis.io/)分布式数据库和[scrapy](https://github.com/scrapy/scrapy)框架。
    你可以将该爬虫和对应的redis节点部署在不同机器上以提高爬取的速度（大概吧）。
 2. 这个工程中的可视化部分基于[matplotlib](https://github.com/matplotlib/matplotlib)开发，这是一个python的数学作图库。   
 3. 数据分析中涉及的一些算法可以在这里查看更多细节：     
    [梯度下降法](http://m.blog.csdn.net/article/details?id=51554910)用于估计播放、硬币、收藏、回复的比值，但是看起来这几个特性不不符合线性关系。   
    [局部权重线性回归](http://www.cnblogs.com/MrLJC/p/4147697.html)被用于估计视频的播放量，这个算法使用和目标视频相近的样本点来估计。    
 4. 分词系统基于[jieba](https://github.com/fxsjy/jieba)中文分词系统，添加了一些bilibili中常用的术语。        

## 环境需求 ##
Pyhton 3.4  
Ruby 2.x  
scarpy  
scrapy-redis  
redis-py  
redis-py-cluster   
matplotlib   
pymysql   
jieba   
## 进度 ##
该工程目前基本可以运行。⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄   
使用10个爬虫实例和2天时间爬取了90万条游戏分类的视频信息样本。
通过做出视频信息样本的3d图标，给我们提供了宏观分析数据的视图。      
使用样本训练局部权重回归算法，并用它预测视频的播放量，某些样本点误差很大，某些估计良好。    
## 更改 ##

 - 9.21

增加了计算局部权重回归误差的代码，这样可以让我们选择最好的k值。   
增加了前几个提交忘记加了的常数项，这会使误差减小，但是某些情况下，误差依旧很大。   

 - 9.18

增加了局部权重回归算法，这个算法在小范围内更能符合样本。       
增加了包含视频信息样本的sql文件，视频信息样本爬取自bilibili的游戏区。     

 - 9.18

增加了一个对视频名字分词的脚本，这个会帮助我们分析bilibili中最受欢迎的词。       

 - 9.17

增加了脚本以绘制视频信息的3D图表，还存在一些性能问题。（有上千个点的时候非常慢）     

 - 9.12

增加了一个使用BGD的脚本来预测播放量，现在还不够准确因为我们还没有考虑视频up主的热度。（同时，这些特征也不准确符合线性关系）    

 - 9.10

增加了一个梯度下降法的框架，使用他来迭代出播放、硬币、收藏等等参数的比例关系。         

 - 9.3（暂停）

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
Redis集群有时会崩溃且不能修复。   
番剧分类还不能正常爬取。       
Redis集群不支持事物，会造成一些原子性问题。  
还未测试连接redis集群是否真的快于连接SQL数据库。(一些数据和文档推荐使用redis最为数据库，但是我还没有测试哪个更快)     
有些页面需要登录才能访问（需要cookies），但是发送cookies需要额外的代码和带宽。暂时考虑把这些网页暂存起来之后统一爬取。  
现在爬虫不能更新redis中的数据，因为dupefilter会阻止爬虫爬取之前见过的页面。   
试验了一次长时间爬取，爬取结束时并没有爬取到所有预计的页面。（爬取了90w页面，但是估计有1000w页面左右）    
局部权重回归算法的某些结果依旧误差很大，某些预测的样本不足，我们可能要尝试非线性模型。   
## 未来计划 ##
需要一些字段记录视频up主的热度。   
加入一些代码以分析爬取得到的数据。       
对于高播放视频，分析其回复用户的注册年龄和性别。   
通过一个脚本运行全部的工程。  
部署一个web服务来展示数据和分析结果。  
