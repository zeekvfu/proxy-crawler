#!/usr/bin/env python3
# coding: utf-8
# mimvp.py


import os
import sys
import datetime
import time
import warnings
import logging

from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.selector import Selector

from _scrapy.items import ProxyItem
from common.utility import get_logger
from common.file_utility import FileUtility


class mimvp(Spider):

    name = 'mimvp'
    base_url = 'http://proxy.mimvp.com/'
    starting_page = 'http://proxy.mimvp.com/free.php'


    @classmethod
    def get_script_dir(cls):
        return os.path.dirname(os.path.realpath(__file__))


    @property
    def logger(self):
        return self._logger


    def __init__(self, start_date=None, *args, **kwargs):
        super(mimvp, self).__init__(*args, **kwargs)
        self.start_date = None
        if start_date is None:
            self.start_date = (datetime.date.today() + datetime.timedelta(days=-3)).strftime('%Y-%m-%d')
        else:
            self.start_date = "%s-%s-%s" % (start_date[0:4], start_date[4:6], start_date[6:8])

        script_dir = self.get_script_dir()
        config = FileUtility.load_json_config('%s/../../../../conf/proxy_crawler.config.json' % script_dir)
        timestamp = time.strftime('%Y-%m-%d_%H:%M:%S')
        self._logger = get_logger("%s/../../../../log/%s.%s.log" % (script_dir, self.name, timestamp), config['log_level'])


    def start_requests(self):
        meta = {}
        yield Request(
            url=self.starting_page,
            meta=meta,
            callback=self.parse_starting_page
        )


    def parse_starting_page(self, response):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): ****************************************************************************************************" % this_func_name)
        self.logger.debug("%s(): start ..." % this_func_name)
        self.logger.debug("%s(): base url\t\t\t%s" % (this_func_name, response.url))
        sel = Selector(response)
        channel_list = sel.xpath('//div[@class="proxy_use_bg"]/div[@class="proxy_use"]/div[@class="tag_area"]/a[contains(@id, "tag_") and @class="label" and contains(@href, "free.php?proxy=")]/@href').extract()
        for channel in channel_list:
            link = self.base_url + channel
            self.logger.debug("%s(): channel\t\t\t%s" % (this_func_name, link))
            yield Request(
                url=link,
                meta=response.meta,
                callback=self.parse_proxy_list
            )


    def parse_proxy_list(self, response):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): proxy list\t\t%s" % (this_func_name, response.url))
        sel = Selector(response)
        proxy_list = sel.xpath('//table[@class="table table-bordered table-striped" and @style="table-layout: fixed;"]/tbody/')
        for proxy_record in proxy_list:
            s = str(proxy_record.extract())
            item = ProxyItem()

            # ip
            elements = proxy_record.xpath(u'td[@data-title="IP"]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['ip'] = elements[0]
            # port
            elements = proxy_record.xpath(u'td[@data-title="PORT"]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['port'] = int(elements[0])
            # protocol
            elements = proxy_record.xpath(u'td[@data-title="类型"]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['protocol'] = elements[0]
            # anonymity
            elements = proxy_record.xpath(u'td[@data-title="匿名度"]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['anonymity'] = elements[0]
            # location
            elements = proxy_record.xpath(u'td[@data-title="位置"]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['location'] = elements[0]
            # validation_time
            elements = proxy_record.xpath(u'td[@data-title="最后验证时间"]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['validation_time'] = elements[0]
            if item['validation_time'] < self.start_date:
                # 不再向后翻页
                return

            item['user_name'] = ''
            item['password'] = ''
            item['support_request_type'] = ''
            item['sp'] = ''
            item['source_site'] = self.name
            item['source_url'] = response.url
            yield item



