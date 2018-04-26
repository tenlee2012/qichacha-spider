# coding=utf-8

import re
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from qichacha.config.settings import LOG_DIR
import uuid

from ..items import parse_response


# class QccSpider(scrapy.Spider):
class QccSpider(RedisSpider):
    name = "qichacha"

    index_url = 'https://www.qichacha.com'
    # start_urls = [index_url]
    page_reg = re.compile(r'\S+?prov=(\S+?)&p=(\d+)')

    def parse(self, response):
        # 所有省地区
        area_urls = response.xpath('//*[@id="area"]/ul/li/a/@href')
        if not area_urls:
            return None
        # area_urls = area_urls[:1]
        for url in area_urls:
            next_url = response.urljoin(url.extract())
            yield scrapy.Request(next_url, callback=self.parse_list)

    def print(self, response):
        self.logger.info(response.text)

    def parse_list(self, response):
        details_url = response.xpath('//*[@id="searchlist"]/a/@href')
        if details_url:
            # details_url = details_url[:1]
            # for url in details_url:
            #     self.logger.info(response.urljoin(url.extract()))

            for url in details_url:
                # 详情页
                detail_url = response.urljoin(url.extract())
                yield scrapy.Request(detail_url, callback=self.parse_detail, dont_filter=True)

        next_url = response.css(".next::attr(href)").extract_first()
        if next_url:
            reg_groups = self.page_reg.match(next_url)
            if reg_groups:
                # 下一页
                next_url = self.index_url + '/g_{}_{}.html'.format(reg_groups.group(1), reg_groups.group(2))
                yield scrapy.Request(next_url, callback=self.parse_list)

    def parse_detail(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        if not response.text.startswith('<script>'):
            try:
                company = parse_response(response)
                yield company
            except Exception as e:
                filename = LOG_DIR + str(uuid.uuid1()) + ".html"
                with open(filename, 'w') as f:
                    f.write(response.text)
                self.logger.error({"message": e, "htmlName": filename})

    def err_back(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
