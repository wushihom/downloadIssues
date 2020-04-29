from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse

class DownloadissuesSpiderMiddleware(object):
    def process_response(self, request, response, spider):
        # request: 响应对象所对应的请求对象
        # response: 拦截到的响应对象
        # spider: 爬虫文件中对应的爬虫类 IssuesSpider 的实例对象, 可以通过这个参数拿到 IssuesSpider 中的一些属性或方法
        
        row_response=spider.browser.get(url=request.url)
        time.sleep(5)    # 等待加载,  可以用显示等待来优化.
        # row_response= spider.browser.page_source
        return HtmlResponse(url=spider.browser.current_url,body=row_response,encoding="utf8",request=request)   # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url

class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        # referer = request.url|'https://issues.apache.org/jira/projects/TIKA/issues'
        referer=request.url
        if referer:
            request.headers["referer"] = referer