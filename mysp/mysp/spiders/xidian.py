import scrapy
from mysp import items
from mysp.items import MyspItem
from mysp.middlewares import MyspDownloaderMiddleware, MyspSpiderMiddleware
import time
from datetime import datetime

class XidianSpider(scrapy.Spider):
    name = "xidian" 
    allowed_domains = ["job.xidian.edu.cn"]
    start_urls = ["https://job.xidian.edu.cn/campus/index?domain=xidian&city=&page=1"]

    xidian_next_page=''
    def parse(self, response): 
        item = MyspItem()
        next_page_href = response.css('li[class="next"]>a::attr(href)').extract()
        last_page_href = response.css('li[class="last"]>a::attr(href)').extract()
        if next_page_href != last_page_href: 
            self.xidian_next_page = 'https://job.xidian.edu.cn' + next_page_href[0]
        else:
            self.xidian_next_page = ''
        c_page_url_list = response.css('ul[class="infoList"]>li:nth-child(1)>a')
        try:
            for job in c_page_url_list: 
                driver = MyspDownloaderMiddleware.get_xidian()
                driver.get('https://job.xidian.edu.cn' + job.css('a::attr(href)').extract()[0])
                time.sleep(1)
                item['theme'] = [driver.find_element('css selector', 'a[class="name text-primary"]').text]
                date_text = driver.find_element('css selector', 'div[class="share"]>ul>li:nth-child(1)').text
                date_text=date_text[date_text.find('：') + 1:] 
                if datetime.strptime(date_text,'%Y-%m-%d %H:%M')<datetime.strptime('2021-09-01 00:00','%Y-%m-%d %H:%M'):
                    self.xidian_next_page=''
                    break
                item['date'] = [date_text]
                views_text = driver.find_element('css selector', 'div[class="share"]>ul>li:nth-child(2)').text
                item['view'] = [views_text[views_text.find('：') + 1:]] 
                item['num']=['0']
                yield item
        except:
            pass
        if self.xidian_next_page!='':
            yield scrapy.Request(self.xidian_next_page, callback=self.parse)