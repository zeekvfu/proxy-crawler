#!/usr/bin/python3
# coding: utf-8
# pipelines.py


import os
import time
from scrapy.exceptions import DropItem

from common.utility import load_json_preserving_order, get_logger
from common.http_tools import get_response_delay, set_ip_location


class ETL(object):

    @staticmethod
    def get_script_dir():
        return os.path.dirname(os.path.realpath(__file__))


    def __init__(self, bot_name):
        self.bot_name = bot_name
        # script_dir = get_script_dir.__func__()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.logger = get_logger("%s/../../log/%s.ETL.%s.log" % (script_dir, self.bot_name, time.strftime('%Y-%m-%d_%H:%M:%S')))
        self.logger.debug("__init__(): start ...")
        config = load_json_preserving_order('%s/../../conf/proxy_test.config.json' % script_dir)
        self.testing_websites = config['testing_websites']


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            bot_name = crawler.settings.get('BOT_NAME')
        )


    @classmethod
    def normalize_anonymity(cls, _anonymity):
        anonymity = _anonymity.strip()
        if anonymity == "高匿名":
            anonymity = "highly anonymous"
        elif anonymity == "透明":
            anonymity = "transparent"
        return anonymity


    def process_item(self, item, spider):
        self.logger.debug("process_item(): start ...")
        item['anonymity'] = ETL.normalize_anonymity(item['anonymity'])

        # protocol
        protocol = item['protocol'].strip().upper()
        if protocol != 'HTTP' and protocol != 'HTTPS':
            raise DropItem("process_item(): protocol %s" % protocol)
        item['protocol'] = protocol

        # 代理是否可用
        flag = False
        sites = self.testing_websites[protocol.lower()][0:4]
        if sites is not None:
            for i in range(0, len(sites)):
                item['site_%d_delay' % i] = get_response_delay(self.logger, sites[i], protocol, item['ip'], item['port'])
                if item['site_%d_delay' % i] > 0:
                    flag = True
        if not flag:
            raise DropItem("process_item(): proxy not available!")

        location = set_ip_location(item['ip'], item['location'])
        if location is not None:
            item['location'] = location

        self.logger.debug("process_item(): finish ...")
        return item




