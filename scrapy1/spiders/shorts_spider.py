import scrapy

from scrapy1.items import Scrapy1Item

class Shorts(scrapy.Spider):
    name="shorts"

    start_urls=[
        "https://seamsfriendly.com/collections/shorts"
    ]
    
    def parse(self, response, **kwargs):
        items=Scrapy1Item()
        products=response.css("div.Grid__Cell")
        for i in products:
            href=response.urljoin(i.css("h2 > a::attr('href')").get())
            yield scrapy.Request(href,callback=self.parse_description)
    def parse_description(self, response):
        des=response.css(".ProductMeta__Description > .Rte > p").css('::text').extract()
        price=response.css(".money::text").get()
        title=response.css(".u-h2::text").get().split("\n")[0]
        shades=response.css("variantswatchking").extract()
        colors=[]
        '''for i in shades:
            colors.append(i.css("::attr(orig-value)").get())'''
        urls=response.css(".AspectRatio > .Image--fadeIn")
        image_urls=[]
        for i in urls:
            link=i.css("::attr(data-original-src)").get()
            if(link):
                image_urls.append("https:"+str(link))
        yield {
            'title':title,'price':price,'colors':shades,'description':des,'image_urls':image_urls
        }