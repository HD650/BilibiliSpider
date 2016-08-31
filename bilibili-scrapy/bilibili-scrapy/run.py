from scrapy.crawler import CrawlerProcess
import scrapy.utils.project

if __name__ == '__main__':
    runner = CrawlerProcess(scrapy.utils.project.get_project_settings())
    runner.crawl('video_spider')
    runner.start()