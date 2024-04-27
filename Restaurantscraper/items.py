# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
        Name = scrapy.Field()
        Street_Address = scrapy.Field()
        Zip_Code = scrapy.Field()
        City = scrapy.Field()
        State = scrapy.Field()
        Price_Range = scrapy.Field()
        Phone = scrapy.Field()
        Rating = scrapy.Field()
        Number_of_Reviews = scrapy.Field()
        Menu_Link= scrapy.Field()
        
