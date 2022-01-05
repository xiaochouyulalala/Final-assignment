# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class MyspPipeline:
    def process_item(self, item, spider):
        try:
            dic_item = dict(item)
            if spider.name == 'bupt':
                self.bupt_writer.writerow(dic_item)
            if spider.name == 'xidian':
                self.xidian_writer.writerow(dic_item)
            if spider.name == 'uestc':
                self.uestc_writer.writerow(dic_item)
            return item
        except Exception as err:
            print("ERROR")
            print("**********************************************************************")
            print(item)
            print("**********************************************************************")
            
    def open_spider(self,spider):
        self.bupt_file =open('BEIYOU_1.csv', 'w+', newline='', encoding='utf-8')
        self.bupt_writer = csv.DictWriter(self.bupt_file,fieldnames=['theme','date','view','num'])
        self.bupt_writer.writeheader()
        self.xidian_file =open('XIDIAN_1.csv', 'w+', newline='', encoding='utf-8')
        self.xidian_writer = csv.DictWriter(self.xidian_file,fieldnames=['theme','date','view','num'])
        self.xidian_writer.writeheader()
        self.uestc_file =open('CHENGDIAN_1.csv', 'w+', newline='', encoding='utf-8')
        self.uestc_writer = csv.DictWriter(self.uestc_file,fieldnames=['theme','date','view','num'])
        self.uestc_writer.writeheader()
    def close_spider(self, spider):
        self.bupt_file.close()
        self.xidian_file.close() 
        self.uestc_file.close()  
        #self.pku_file.close()  