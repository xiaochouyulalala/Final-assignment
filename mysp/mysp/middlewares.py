# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium import webdriver
import time
import scrapy


class MyspSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyspDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    @classmethod
    def __init__(cls):
        cls.bupt_driver = webdriver.Chrome()
        cls.xidian_driver = webdriver.Chrome()
        cls.uestc_driver = webdriver.Chrome()

    @classmethod
    def __del__(cls):
        cls.bupt_driver.close()
        cls.xidian_driver.close()
        cls.uestc_driver.close()
    
    @classmethod
    def get_bupt(cls):
        return cls.bupt_driver
    @classmethod
    def get_xidian(cls):
        return cls.xidian_driver
    @classmethod
    def get_uestc(cls):
        return cls.uestc_driver

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == 'bupt':
            self.bupt_driver.get(request.url)
            time.sleep(5)
            return scrapy.http.HtmlResponse(url=request.url, body=self.bupt_driver.page_source.encode('utf-8'),
                                            encoding='utf-8', request=request, status=200)
        elif spider.name == 'xidian':
            self.xidian_driver.get(request.url)
            time.sleep(5)
            return scrapy.http.HtmlResponse(url=request.url, body=self.xidian_driver.page_source.encode('utf-8'),
                                            encoding='utf-8', request=request, status=200)
        elif spider.name == 'uestc':
            self.uestc_driver.get(request.url)
            time.sleep(5)
            return scrapy.http.HtmlResponse(url=request.url, body=self.uestc_driver.page_source.encode('utf-8'),
                                            encoding='utf-8', request=request, status=200)


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
