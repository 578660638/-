# -*- coding: utf-8 -*-
import scrapy
import json, re
from ..items import JintangItem

class JinSpider(scrapy.Spider):
    name = 'jin'
    allowed_domains = ['sztjgold.com']
    start_urls = ['https://www.sztjgold.com/files/0/91/91.json?cdnversions=5254587']
    #创建字典items通道里的
    items = JintangItem()

    def parse(self, response):
        a = response.text

        a1 = json.loads(a)
        if a1.get('list'):
            for text in a1['list']:
                if text.get('chaptername'):
                    #获取id ,name,id用来翻页，name用来给文件命名
                    JinSpider.items['id2'] = text.get('chapterid')
                    JinSpider.items['name2'] = text.get('chaptername')
                    id3=text.get('chapterid')
                    url = f"https://www.sztjgold.com/files/article/html555/1/1427/{JinSpider.items['id2']}.html"
                    #具体哪一集回交给xiangqing函数
                    yield scrapy.Request(url, callback=self.xiangqing)
                    yield JinSpider.items

    def xiangqing(self, response):
        a1 = response.text
        a1 = re.findall("[\u4E00-\u9FFF]", a1)
        # ------------------------------<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;
        a1 = str(a1)
        # 清洗字符串
        a1 = a1.replace(',', '')
        a1 = a1.replace("'", '')
        a1 = a1.replace('茵 右 脚 楞 夺', "")
        a1 = a1.replace('夺 粗 功 肖 功 地', '')
        a1 = a1.replace('顺 困 顶 枯 枵', '')
        a1 = a1.replace('夺 回 顾 功 带 困', '')
        a1 = a1.replace(' 顶 置 中', '')
        JinSpider.items['text2'] = a1

