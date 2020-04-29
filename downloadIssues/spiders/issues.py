# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
# from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
import time
#无头浏览器设置
# chrome_options = Options()
# chorme_options.add_argument("--headless")
# chorme_options.add_argument("--disable-gpu")

class IssuesSpider(scrapy.Spider):
    name = 'issues'
    # allowed_domains = ['https://issues.apache.org/jira/browse']
    start_urls = ['https://issues.apache.org']
    def __init__(self):
        self.browser = webdriver.Chrome()
        super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            self.browser.get(url)
            self.browser.find_element_by_xpath('//html/body/ul/li[4]/a').click()
            time.sleep(60)
            self.browser.find_element_by_id('quickSearchInput').send_keys('TIKA')
            time.sleep(10)
            self.browser.find_element_by_xpath('//*[@id="quicksearch"]/div[1]/div[2]/ul/li[1]/a').click()
            time.sleep(60)
            print(self.browser.page_source)

        
    def parse(self, response):
        div_list = response.xpath("//div[@class='issue-link-key']/@text").extract()
        for index in div_list:
            response = scrapy.Request('https://issues.apache.org/jira/browse/{0}'.format(div_list[index]),callback=self.parse_detail)
            yield response

        next_url = response.xpath("//a[@class='nav-next']/@href").extract()
        
        if next_url:
            yield scrapy.Request(next_url[0],callback=self.parse)

        

    def parse_detail(self,response):
        name = response.xpath("//div[@class='attachment-thumb']/a/@text").extract()
        url = response.xpath("//div[@class='attachment-thumb']/a/@href").extract()

        item = DownloadissuesItem()

        item['name'] = name
        item['file_urls'] = url

        yield item

