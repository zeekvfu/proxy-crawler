#!/usr/bin/python3
# coding: utf-8
# kuaidaili.py


import os
import sys
import datetime
import logging

from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.selector import Selector

from _scrapy.items import ProxyItem
from common.utility import get_logger




class kuaidaili(Spider):
    @staticmethod
    def get_script_dir():
        return os.path.dirname(os.path.realpath(__file__))


    name = 'kuaidaili'
    base_url = "http://www.kuaidaili.com"
    starting_page = "%s/free/" % (base_url)
    logger = get_logger("%s/../../../log/%s.log" % (get_script_dir.__func__(), name))


    def __init__(self, start_date=None, *args, **kwargs):
        super(kuaidaili, self).__init__(*args, **kwargs)
        if start_date is None:
            self.start_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        else:
            self.start_date = "%s-%s-%s" % (start_date[0:4], start_date[4:6], start_date[6:8])


    def start_requests(self):
        meta = {}
        yield Request(
            url=self.starting_page,
            meta=meta,
            callback=self.parse_base_url
        )


    def parse_base_url(self, response):
        self.logger.debug("****************************************************************************************************")
        self.logger.debug("parse_base_url(): base url\t\t\t%s" % (response.url))
        sel = Selector(response)
        channel_list = sel.xpath('//div/div[@class="tag_area2"]/a[contains(@id, "tag_") and contains(@class, "label") and contains(@href, "/free/")]/@href').extract()
        for channel in channel_list:
            link = self.base_url + channel
            self.logger.debug("parse_base_url(): channel\t\t\t%s" % (link))
            yield Request(
                url=link,
                meta=response.meta,
                callback=self.parse_proxy_list
            )


    def parse_proxy_list(self, response):
        self.logger.debug("parse_proxy_list(): proxy list\t\t%s" % (response.url))
        # 是否向后翻页
        flag = True
        sel = Selector(response)
        proxy_list = sel.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for proxy_record in proxy_list:
            item = ProxyItem()
            # ip
            elements = proxy_record.xpath(u'td[@data-title="IP"]/text()').extract()
            if len(elements) != 1:
                return
            item['ip'] = elements[0]
            # port
            elements = proxy_record.xpath(u'td[@data-title="PORT"]/text()').extract()
            if len(elements) != 1:
                return
            item['port'] = elements[0]
            # protocol
            elements = proxy_record.xpath(u'td[@data-title="类型"]/text()').extract()
            if len(elements) != 1:
                return
            item['protocol'] = elements[0]
            # anonymity
            elements = proxy_record.xpath(u'td[@data-title="匿名度"]/text()').extract()
            if len(elements) != 1:
                return
            item['anonymity'] = elements[0]
            # location
            elements = proxy_record.xpath(u'td[@data-title="位置"]/text()').extract()
            if len(elements) != 1:
                return
            item['location'] = elements[0]
            # response_delay_in_ms
            elements = proxy_record.xpath(u'td[@data-title="响应速度"]/text()').extract()
            if len(elements) != 1:
                return
            item['response_delay_in_ms'] = elements[0]
            # validation_time
            elements = proxy_record.xpath(u'td[@data-title="最后验证时间"]/text()').extract()
            if len(elements) != 1:
                return
            item['validation_time'] = elements[0]
            if item['validation_time'] < self.start_date:
                flag = False
                break
            item['source'] = self.name
            yield item
        if flag:
            yield self.turn_to_next_page(response)


    # 翻页
    def turn_to_next_page(self, response):
        self.logger.debug("turn_to_next_page(): current page\t%s" % (response.url))
        sel = Selector(response)
        next_page_list = sel.xpath(u'//div[@id="listnav"]/ul/li/a[@class="active"]/../following-sibling::li/a/@href').extract()
        if len(next_page_list) == 0:
            return
        link = self.base_url + next_page_list[0]
        self.logger.debug("turn_to_next_page(): next page\t\t%s" % (link))
        return Request(
            url=link,
            meta=response.meta,
            callback=self.parse_proxy_list
        )




