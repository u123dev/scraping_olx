from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils import spider
from scrapy.utils.project import get_project_settings

from olx.spiders.olx_spider import OlxSpider


@shared_task(queue="scraping_queue")
def start_scraping():
    spider.logger.info("Scraping task started!")

    process = CrawlerProcess(get_project_settings())
    process.crawl(OlxSpider)
    process.start()

    spider.logger.info("Scraping task finished!")


if __name__ == '__main__':
    start_scraping()
