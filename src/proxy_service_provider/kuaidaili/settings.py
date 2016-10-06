#!/usr/bin/python3
# coding: utf-8
# settings.py


import os
import time
from common.file_utility import write_to_file


# 获取脚本所在的路径
def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))

script_dir = get_script_dir()


BOT_NAME = 'kuaidaili_spider'
SPIDER_MODULES = ['proxy_service_provider.kuaidaili.spiders']
NEWSPIDER_MODULE = 'proxy_service_provider.kuaidaili.spiders'


FEED_FORMAT = 'csv'
# 尽量提取、保留所有字段
FEED_EXPORT_FIELDS = [
        "protocol", 
        "ip", 
        "port", 
        "user_name", 
        "password", 
        "anonymity", 
        "support_request_type", 
        "location", 
        "sp", 
        "validation_time", 
        "source"
        ]

# FEED_URI = script_dir + '/../../../output/%(name)s.%(time)s.csv'
FEED_URI = '%s/../../../output/%s.%s.csv' % (script_dir, BOT_NAME, time.strftime('%Y-%m-%d_%H:%M:%S'))
FEED_URI = os.path.realpath(FEED_URI)
write_to_file('%s/../../../output/proxy_crawler.output' % script_dir, FEED_URI + '\n')

CSV_DELIMITER = '\t'
FEED_EXPORTERS = {
        'csv': '_scrapy.exporters.CsvOptionRespectingItemExporter'
        }


LOG_LEVEL = 'INFO'
LOG_FILE = '%s/../../../log/%s.%s.log' % (script_dir, BOT_NAME, time.strftime('%Y-%m-%d_%H:%M:%S'))


ITEM_PIPELINES = {
        'proxy_service_provider.kuaidaili.pipelines.ETL': 0
        }


DOWNLOAD_DELAY = 3


EXTENSIONS = {
        }


CONCURRENT_REQUESTS_PER_DOMAIN = 500
CONCURRENT_REQUESTS = 1000
CLOSESPIDER_ERRORCOUNT = 50
REACTOR_THREADPOOL_MAXSIZE = 200


USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0"


