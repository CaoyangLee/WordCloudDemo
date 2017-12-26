# -*- coding: utf-8 -*-
import scrapy
from ..items import CommentItem
import time
import requests
import random


# 《芳华》短评
class CommentSpider(scrapy.Spider):
    page = 1
    name = 'comment'
    login = False

    # allowed_domains = ['movie.douban.com']
    # start_urls = ['https://www.douban.com/login']

    def go_login(self, response):
        if not self.login:
            captcha = response.css('div.item-captcha')
            self.login = True
            if captcha:
                code_url = response.css('div.item-captcha img::attr(src)').extract_first().strip()

                try:
                    pic = requests.get(code_url, timeout=20)
                except requests.exceptions.ConnectionError:
                    print('errow image can\'t download')

                print('正在下载---' + '验证码.jpg')
                with open('验证码.jpg', 'wb') as f:
                    f.write(pic.content)

                code = input('请输入验证码:')
                print("登录1")
                yield scrapy.FormRequest('https://www.douban.com/login',
                                         formdata={'form_email': '15860371899',
                                                   'form_password': '20160101zz',
                                                   'captcha-solution': code},
                                         callback=self.logged_success)
            else:
                print("登录2")
                yield scrapy.FormRequest('https://www.douban.com/login',
                                         formdata={'form_email': '15860371899', 'form_password': '20160101zz'},
                                         callback=self.logged_success)

    def start_requests(self):
        return [scrapy.Request('https://www.douban.com/login', callback=self.go_login),]

    def logged_success(self, response):
        print('========================')
        print('登录完成')
        print('========================')
        yield scrapy.Request('https://movie.douban.com/subject/26862829/comments', callback=self.parse)

    def parse(self, response):
        print('是否登录', self.login)

        print('开始')
        for item in response.css('div.comment'):
            comment = CommentItem()
            comment['content'] = item.css('p::text').extract_first().strip()
            yield comment

        print('========================')
        print('第%s页加载完成' % self.page)
        self.page = self.page + 1
        print('========================')

        next_page = response.css('div#paginator a.next::attr(href)').extract_first()
        if next_page is not None:
            time.sleep(random.randint(0,9))
            yield response.follow(next_page, self.parse)
