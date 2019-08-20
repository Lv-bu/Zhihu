# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item,Field


class ZhihuuserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=Field()
    name=Field()
    avatar_url=Field()
    headline=Field()
    gender=Field()
    id=Field()
    type=Field()
    url=Field()
    url_token=Field()
    use_default_avatar=Field()
    user_type=Field()
    answer_count=Field()
    articles_count=Field()
    badge=Field()
    follower_count=Field()




