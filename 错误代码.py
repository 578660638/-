import scrapy
from snbook.items import SnbookItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['https://list.suning.com/1-502322-0.html']

    def parse(self, response):
        list1 = response.xpath('//ul[@class="clearfix"]')
        for i in list1:
            item = SnbookItem()
            item['bookname'] = i.xpath('.//p[@class="sell-point"]/a/text()').get()
            item['price'] = i.xpath('.//em[@class="prive price"]/text()').get()
            #半截网址进行拼接
            item['bookurl'] = i.xpath('.//p[@class="sell-point"]/a/@href').getall()
            item['bookurl'] = ['https:' + i for i in item['bookurl']]
            for url in item['bookurl']:
                yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail)


    def parse_detail(self, reponse):
        item = reponse.meta['item']
        # price = reponse.xpath('//div[@class="wrapper proinfo"]//span[@class="mainprice"]/text()')
        price = reponse.xpath('//div[@class="wrapper proinfo"]//li[2]/text()').getall()
        item['price'] = price
        print(item)
