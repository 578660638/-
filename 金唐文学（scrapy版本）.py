# -*- coding: utf-8 -*-
import scrapy
import json, re
from ..items import JintangItem
import requests


class JinSpider(scrapy.Spider):
    name = 'jin'
    allowed_domains = ['sztjgold.com']
    start_urls = ['https://www.sztjgold.com/files/0/19/19.json?cdnversions=5254959']
    # items = JintangItem()
    # 创建字典items通道里的


    def xiangqing(self, a):
        # print(a)
        item = {}
        name3 = a.meta['name3']
        a=a.text
        a=str(a)
        # print(a.text)
        # a = a.text
        a1 = re.findall("[\u4E00-\u9FFF]", a)
        # # ------------------------------<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;
        a1 = str(a1)
        # 清洗字符串
        a1 = a1.replace(',', '')
        a1 = a1.replace(' ','')
        a1 = a1.replace("'", '')
        a1 = a1.replace('茵右脚楞夺', "")
        a1 = a1.replace('夺粗功肖功地', '')
        a1 = a1.replace('顺困顶枯枵', '，')
        a1 = a1.replace('夺回顾功带困', '')
        a1 = a1.replace('顶置中', '')
        item['text2'] = a1
        item['name3'] = name3
        yield item

    def parse(self, response):
        a = response.text
        # 判断网页中响应是不是有"chapterid",如果没有执行else
        if '"chapterid"' in a:
            # 有的话转换成json类型
            a1 = json.loads(a)
            if a1.get('list'):
                for dat in a1['list']:

                    #获取id ,name,id用来翻页，name用来给文件命名
                    #item['id2'] = text.get('chapterid')

                    id3 = dat.get('chapterid')
                    name3 = dat.get('chaptername')
                    url1 = f'https://www.sztjgold.com/files/article/html555/0/426/{id3}.html'
                    mate = {'name3': name3}
                    yield scrapy.Request(url1, callback=self.xiangqing, meta=mate)
                    # print(JinSpider.item)

        # 详情页处理

        # print(JinSpider.item.values())

        # def xiangqing(self, response):
        #     a1 = response.text
        #     a1 = re.findall("[\u4E00-\u9FFF]", a1)
        #     # ------------------------------<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;
        #     a1 = str(a1)
        #     # 清洗字符串
        #     a1 = a1.replace(',', '')
        #     a1 = a1.replace("'", '')
        #     a1 = a1.replace('茵 右 脚 楞 夺', "")
        #     a1 = a1.replace('夺 粗 功 肖 功 地', '')
        #     a1 = a1.replace('顺 困 顶 枯 枵', '')
        #     a1 = a1.replace('夺 回 顾 功 带 困', '')
        #     a1 = a1.replace(' 顶 置 中', '')
        #     JinSpider.items['text2'] = a1
