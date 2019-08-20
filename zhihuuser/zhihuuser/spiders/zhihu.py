# -*- coding: utf-8 -*-
import json
import scrapy
from zhihuuser.items import ZhihuuserItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    #选定一个人
    start_user='excited-vczh'

    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'    #Request URL
    user_query='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics' #include

    #关注列表的接口
    follows_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    # 粉丝列表的接口
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        #url='https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=40&limit=20'
        yield scrapy.Request(self.user_url.format(user=self.start_user,include=self.user_query),self.parse_user)#获取该用户信息，然后请求
        yield scrapy.Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)#请求关注列表
        yield scrapy.Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),self.parse_followers)#请求粉丝列表

    #解析user的详细信息，赋值给item
    def parse_user(self, response):
        result=json.loads(response.text)
        item=ZhihuuserItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield item
        #再获取关注列表中每个人的关注列表
        yield scrapy.Request(
            self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),self.parse_follows)
        # 再获取粉丝列表中每个人的关注列表
        yield scrapy.Request(
            self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20, offset=0),self.parse_followers)

    #处理关注列表
    def parse_follows(self, response):
        results = json.loads(response.text)

        #获取关注列表的每一个人的信息
        if 'data' in results.keys():
            for result in results.get('data'):                                                                      #callback
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),self.parse_user)
        # 关注列表有多页的情况，判断分页是否结束，若还没结束，获取下一页的关注列表
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page,self.parse_follows)

    # 处理粉丝列表
    def parse_followers(self, response):
        results = json.loads(response.text)

        # 获取关注列表的每一个人的信息
        if 'data' in results.keys():
            for result in results.get('data'):  # callback
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),self.parse_user)
        # 粉丝列表有多页的情况，判断分页是否结束，若还没结束，获取下一页的粉丝列表
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, self.parse_followers)