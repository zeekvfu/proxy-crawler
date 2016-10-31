#!/usr/bin/env python3
# coding: utf-8
# xicidaili.py


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
from util.utility import get_logger, trim_blank_lines_in_list
from util.file_utility import FileUtility


class xicidaili(Spider):

    name = 'xicidaili'
    base_url = 'http://www.xicidaili.com'
    starting_page = base_url


    @classmethod
    def get_script_dir(cls):
        return os.path.dirname(os.path.realpath(__file__))


    @property
    def logger(self):
        return self._logger


    def __init__(self, start_date=None, *args, **kwargs):
        super(xicidaili, self).__init__(*args, **kwargs)
        self.start_date = None
        if start_date is None:
            self.start_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%y-%m-%d %H:%M')
        else:
            self.start_date = "%s-%s-%s" % (start_date[2:4], start_date[4:6], start_date[6:8])

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
        channel_list = sel.xpath('//div[@id="header"]/ul[@id="nav"]/li[position()>=3 and position()<=6]/a/@href').extract()
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
        proxy_list = sel.xpath('//table[@id="ip_list"]/tr[@class and position()>1]')
        # proxy_list = sel.xpath('//table[@id="ip_list"]/tbody[@class]/tr[@class and position()>1]')
        for proxy_record in proxy_list:
            s = str(proxy_record.extract())
            item = ProxyItem()

            # ip
            elements = proxy_record.xpath(u'td[position()=2]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['ip'] = elements[0]
            # port
            elements = proxy_record.xpath(u'td[position()=3]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['port'] = int(elements[0])
            # location
            elements = proxy_record.xpath(u'td[position()=4]//text()').extract()
            if len(elements) != 1:
                # warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                pass
            item['location'] = '\n'.join(trim_blank_lines_in_list(elements))
            # anonymity
            elements = proxy_record.xpath(u'td[position()=5]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['anonymity'] = elements[0]
            # protocol
            elements = proxy_record.xpath(u'td[position()=6]/text()').extract()
            if len(elements) != 1:
                warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                continue
            item['protocol'] = elements[0]
            # validation_time
            elements = proxy_record.xpath(u'td[position()=10]/text()').extract()
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
            item['source_url'] = ''
            yield item

        yield self.turn_to_next_page(response)


    # 翻页
    def turn_to_next_page(self, response):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): current page\t%s" % (this_func_name, response.url))
        sel = Selector(response)
        next_page_list = sel.xpath(u'//div[@class="pagination"]/a[@class="next_page" and @rel="next" and text()="下一页 ›"]/@href').extract()
        if len(next_page_list) == 0:
            return
        link = self.base_url + next_page_list[0]
        self.logger.debug("%s(): next page\t\t%s" % (this_func_name, link))
        return Request(
            url=link,
            meta=response.meta,
            callback=self.parse_proxy_list
        )




