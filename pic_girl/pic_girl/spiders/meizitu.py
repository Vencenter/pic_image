# -*- coding: utf-8 -*-
import scrapy
from pic_girl.items import PicGirlItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor


class MeiziSpider(CrawlSpider):
    name = "meizitu"
    allowed_domains = ["mzitu.com"]
    start_urls = ['http://www.mzitu.com/']
    img_urls=[]

    rules = (
        Rule(LinkExtractor(allow=('/\d{6}',)),\
             callback='parser_item',follow=True),
           )

    def parser_item(self,response):
        item=PicGirlItem()
        name=response.selector.xpath('/html/body/div[2]/div[1]/div[1]/text()[3]').extract()
        item['name']=name[0][3:-1]
        item['url']=response.url
        all_page=response.selector.xpath('/html/body/div[2]/div[1]/div[4]/a[5]/span/text()').extract()
        for page in range(1,int(all_page[0])+1):
            url=response.url+'/'+str(page)
            #print "url =====>",url
            yield scrapy.Request(url=url,callback=self.img_url, dont_filter=True)
        item['img_url']=self.img_urls
        yield item
    def img_url(self,response):
        urls=response.selector.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@src').extract()
        for img_url in urls:
            f =open("data.txt","a+")
            f.write(img_url+"\n")
            f.close()
            print img_url+"    ===>>download"
            self.img_urls.append(img_url)



