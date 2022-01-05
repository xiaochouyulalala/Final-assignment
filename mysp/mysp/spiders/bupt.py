import scrapy
from mysp import items
from mysp.items import MyspItem
from mysp.middlewares import MyspDownloaderMiddleware, MyspSpiderMiddleware
import time
from datetime import datetime

class BuptSpider(scrapy.Spider):
    name = 'bupt'
    allowed_domains = ['https://job.bupt.edu.cn/']
    start_urls = ['https://job.bupt.edu.cn/frontpage/bupt/html/recruitmentinfoList.html?type=1']
    
    def parse(self, response):
        item = MyspItem()
        index = 0
        web_driver = MyspDownloaderMiddleware.get_bupt()
        web_driver.get('https://job.bupt.edu.cn/frontpage/bupt/html/recruitmentinfoList.html?type=1')
        web_driver.maximize_window()
        bupt_list=[]
        #next_page = web_driver.find_elements('css selector','ul[class="fPage"]>li>a[class="next"]')[1]
        while(1):
            index+=1        
            time.sleep(1)
            leng = len(web_driver.find_elements('css selector','div[class="left"]>a'))
            for i in range(leng):
                bupt_list.append(web_driver.find_elements('css selector','div[class="left"]>a')[i].get_attribute("href"))
            next_page = web_driver.find_elements('css selector','ul[class="fPage"]>li>a[class="next"]')[1]
            next_page.click()
            if(index>55):
                break
        for each in bupt_list:
            try:
                web_driver.get(each)
                time.sleep(0.5)
                item['theme'] = [web_driver.find_element('css selector','div[class="name getCompany"]').text]
                text = web_driver.find_element('css selector','div[class="midInfo"]>div[class="l_con"]').text
                date_text = text[text.find('日期')+3:text.find('浏览次数')-3]
                """
                    发布企业：中国华腾工业有限公司     日期：2021-12-30      浏览次数：301
                """          
                if datetime.strptime(date_text,'%Y-%m-%d')<datetime.strptime('2021-09-01','%Y-%m-%d'):
                    break
                item['date'] = [date_text]
                view_text = text[text.find('浏览次数')+5:]
                item['view'] = [view_text]    
                num_text = web_driver.find_element('css selector','div[class="infoLeft"]>div[class="desc"]>span:nth-child(1)').text
                num_text = num_text[:num_text.find('个职位')]
                item['num'] = [num_text]
            except Exception as err:
                print("ERROR")
                item['num']=['1']
            finally:
                yield item



















