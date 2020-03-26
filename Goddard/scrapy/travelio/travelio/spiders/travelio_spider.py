import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest

class TravelioApartLink(scrapy.Spider):
    def __init__(self):
        self.links = []
    
    name = 'travelio'
    allowed_domains=["travelio.com"]
    start_urls = [
        'https://www.travelio.com/sewa-apartemen-jakarta?page=1'
    ]

    def parse(self, response):
        apartments = response.css('div.property-box')
        for apart in apartments:
            link = apart.css('a[href*=travelio]').attrib['href']    
            self.links.append("https:%s" % link)
            self.log("Links %s" % self.links)
            yield SplashRequest(url="https:%s" % link, callback=self.parse_detail_apart, args={
                'timeout': 90,
                'wait': 2.5
            })
    
    def parse_detail_apart(self, response):
        name = response.xpath("//div[@id='hotel-name']/h2/text()").get()
        facility_title = response.xpath("//span[@class='hotel-left-head-title']/text()").getall()
        kamar_facility = response.xpath("//div[@id='hotel-room-detail']/div[@class='hotel-left-item-info-wrapper']/div[@class='hotel-left-item-info']/div[@class='hotel-left-item-info-head']/text()").getall()
        detail_facility = response.css("div.hotel-left-item-info-head::text").getall()
        value_facility = response.css("div.hotel-left-item-info-detail::text").getall() 
        self.log("Apart name : %s" % name)
        self.log("Facility Title: %s" % facility_title)
        self.log("Kamar facility: %s" % kamar_facility)
        self.log("Detail facility: %s" % detail_facility)
        self.log("Value facility: %s" % value_facility)

    
    
