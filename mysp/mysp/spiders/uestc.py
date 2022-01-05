import scrapy
from mysp import items
from mysp.items import MyspItem
from mysp.middlewares import MyspDownloaderMiddleware, MyspSpiderMiddleware
import time
from datetime import datetime

class UestcSpider(scrapy.Spider):
    name = 'uestc'
    allowed_domains = ['https://yjsjob.uestc.edu.cn/']
    start_urls = ['https://yjsjob.uestc.edu.cn/coread/more-eminfo.jsp']

    def parse(self, response):
        item = MyspItem()
        ue_driver = MyspDownloaderMiddleware.get_uestc()
        ue_driver.get('https://yjsjob.uestc.edu.cn/coread/more-eminfo.jsp')
        ue_driver.maximize_window()
        index = 0
        while(1):
            index+=1        
            time.sleep(1)
            if(index>110):
                break
            try:
                leng = len(ue_driver.find_elements('css selector','div[class="event-content"]>h6>a'))
                
                for i in range(leng):
                    time.sleep(0.1)
                    item['theme'] = [ue_driver.find_elements('css selector','div[class="event-content"]>h6>a')[i].text]
                    date_text = ue_driver.find_elements('css selector','ul[class="event-meta"]>li:nth-child(2)')[i].text  
                    text = date_text[date_text.find(":")+1:]
                    date_text = text[:text.find("年")]+"-"+text[text.find("年")+1:text.find("月")]+"-"+text[text.find("月")+1:text.find("日")]
                    if datetime.strptime(date_text,'%Y-%m-%d')<datetime.strptime('2021-09-01','%Y-%m-%d'):
                        break
                    item['date'] = [date_text]
                    view_text =ue_driver.find_elements('css selector','ul[class="event-meta"]>li:nth-child(1)')[i].text
                    view_text = view_text[view_text.find(":")+1:]
                    item['view'] = [view_text]
                    item['num'] = ['0']
                    print(item)
                    yield item
            except Exception as err:
                print("ERROR")
               # print("***********EEEEEEEEEEEEEEEEEEEEEEEEEEE*******************************")
            next_page = ue_driver.find_element('css selector','ul[class="pagination"]>li>a[title="Go to next page"]')
            next_page.click()




















