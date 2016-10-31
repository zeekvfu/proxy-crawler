#!/usr/bin/env python3
# coding: utf-8
# cn_proxy.py


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


class cn_proxy(Spider):

    name = 'cn_proxy'
    china_proxy_page = 'http://cn-proxy.com/'
    global_proxy_page = 'http://cn-proxy.com/archives/218'


    @classmethod
    def get_script_dir(cls):
        return os.path.dirname(os.path.realpath(__file__))


    @property
    def logger(self):
        return self._logger


    def __init__(self, start_date=None, *args, **kwargs):
        super(cn_proxy, self).__init__(*args, **kwargs)
        self.start_date = None
        if start_date is None:
            self.start_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.start_date = "%s-%s-%s" % (start_date[0:4], start_date[4:6], start_date[6:8])

        script_dir = self.get_script_dir()
        config = FileUtility.load_json_config('%s/../../../../conf/proxy_crawler.config.json' % script_dir)
        timestamp = time.strftime('%Y-%m-%d_%H:%M:%S')
        self._logger = get_logger("%s/../../../../log/%s.%s.log" % (script_dir, self.name, timestamp), config['log_level'])


    def start_requests(self):
        this_func_name = sys._getframe().f_code.co_name
        self.logger.debug("%s(): ****************************************************************************************************" % this_func_name)
        self.logger.debug("%s(): start ..." % this_func_name)
        yield Request(url=self.china_proxy_page, 
                callback=self.parse_proxy_page, 
                meta={'proxy_type': 'china'})

        yield Request(url=self.global_proxy_page, 
                callback=self.parse_proxy_page, 
                meta={'proxy_type': 'global'})


    def parse_proxy_page(self, response):
        this_func_name = sys._getframe().f_code.co_name
        proxy_type = response.meta['proxy_type']
        self.logger.debug("%s(): proxy_type: %s\tproxy page: %s" % (this_func_name, proxy_type, response.url))
        sel = Selector(response)
        tables = sel.xpath('//table[@class="sortable"]/tbody')
        for table in tables:
            proxy_list = table.xpath(u'tr')
            for proxy_record in proxy_list:
                s = str(proxy_record.extract())
                item = ProxyItem()

                # ip
                elements = proxy_record.xpath(u'td[position()=1]/text()').extract()
                if len(elements) != 1:
                    warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                    continue
                item['ip'] = elements[0]

                # port
                elements = proxy_record.xpath(u'td[position()=2]/text()').extract()
                if len(elements) != 1:
                    warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                    continue
                item['port'] = int(elements[0])

                # anonymity
                item['anonymity'] = ''
                if proxy_type == 'global':
                    elements = proxy_record.xpath(u'td[position()=3]//text()').extract()
                    if len(elements) != 1:
                        warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                        continue
                    item['anonymity'] = '\n'.join(trim_blank_lines_in_list(elements))

                # location
                location_pos = 3
                if proxy_type == 'global':
                    location_pos = 4
                elements = proxy_record.xpath(u'td[position()=%d]//text()' % location_pos).extract()
                if len(elements) != 1:
                    warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                    continue
                item['location'] = '\n'.join(trim_blank_lines_in_list(elements))

                # validation_time
                elements = proxy_record.xpath(u'td[position()=last()]/text()').extract()
                if len(elements) != 1:
                    warnings.warn("\t%s(): len(elements)!=1\t%s\t%s" % (this_func_name, s, str(elements)))
                    continue
                item['validation_time'] = elements[0]
                if item['validation_time'] < self.start_date:
                    return

                item['protocol'] = ''
                item['user_name'] = ''
                item['password'] = ''
                item['support_request_type'] = ''
                item['sp'] = ''
                item['source_site'] = self.name
                item['source_url'] = ''

                yield item




