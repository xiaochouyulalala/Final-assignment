# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspItem(scrapy.Item):
    theme = scrapy.Field()
    date = scrapy.Field()
    view = scrapy.Field()
    num = scrapy.Field()
    pass
