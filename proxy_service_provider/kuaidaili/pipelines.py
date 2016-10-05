#!/usr/bin/python3
# coding: utf-8
# pipelines.py


import os
import time
from scrapy.exceptions import DropItem

from common.utility import load_json_preserving_order, get_logger
from common.tools import get_response_delay


class ETL(object):

    @staticmethod
    def get_script_dir():
        return os.path.dirname(os.path.realpath(__file__))


    def __init__(self, bot_name):
        self.bot_name = bot_name
        # script_dir = get_script_dir.__func__()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.logger = get_logger("%s/../../log/%s.pipeline_ETL.%s.log" % (script_dir, self.bot_name, time.strftime('%Y-%m-%d %H:%M:%S')))
        self.logger.debug("__init__(): start ...")
        config = load_json_preserving_order('%s/../../conf/config.json' % script_dir)
        self.http_sites = config['delay_testing_sites']['http'][0:4]
        self.https_sites = config['delay_testing_sites']['https'][0:4]


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
        protocol = item['protocol'].strip().upper()
        sites = None
        if protocol == 'HTTP':
            sites = self.http_sites
        elif protocol == 'HTTPS':
            sites = self.https_sites
        if sites is not None:
            for i in range(1, len(sites)+1):
                item['site_%d_delay' % i] = get_response_delay(self.logger, sites[i], protocol, item['ip'], item['port'])
        self.logger.debug("process_item(): finish ...")
        return item




