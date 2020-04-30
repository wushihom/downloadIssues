# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
#无头浏览器设置
options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")

class IssuesSpider(scrapy.Spider):
    name = 'issues'
    # allowed_domains = ['https://issues.apache.org/jira/browse']
    start_urls = ['https://issues.apache.org']
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=options)
        super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            self.browser.get(url)
            try:
                element1 = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/ul/li[4]/a'))
                )
                # text = self.browser.page_source
                # print("text", text)
                element1.click()
            finally:
                try:
                    element2 = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.ID, 'quickSearchInput'))
                    )
                    # text = self.browser.page_source
                    # print("text", text)
                    element2.send_keys('TIKA')
                finally:
                    try:
                        element3 = WebDriverWait(self.browser, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="quicksearch"]/div[1]/div[2]/ul/li[1]/a'))
                        )
                        element3.click()
                    finally:
                        try:
                            element4 = WebDriverWait(self.browser, 20).until(
                                EC.presence_of_element_located((By.ID, 'content'))
                            )
                            print(element4)
                            yield element4
                        finally:
                            pass
                            # self.browser.quit()
            # self.browser.find_element_by_id('quickSearchInput').send_keys('TIKA')
            # self.browser.find_element_by_xpath('//*[@id="quicksearch"]/div[1]/div[2]/ul/li[1]/a').click()
            
                
            

        
    def parse(self, response):
        div_list = response.xpath("//span[@class='issue-link-key']/@text").extract()
        for index in div_list:
            print(index)
            yield scrapy.Request('https://issues.apache.org/jira/browse/{0}'.format(div_list[index]),callback=self.parse_detail)

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

