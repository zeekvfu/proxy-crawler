#!/usr/bin/python3
# coding: utf-8
# settings.py


import time


BOT_NAME = 'kuaidaili_spider'
SPIDER_MODULES = ['proxy_service_provider.kuaidaili.spiders']
NEWSPIDER_MODULE = 'proxy_service_provider.kuaidaili.spiders'


FEED_FORMAT = 'csv'
FEED_EXPORT_FIELDS = [
        "ip", 
        "port", 
        "protocol", 
        "anonymity", 
        "request_type", 
        "location", 
        "sp", 
        "response_delay_in_ms", 
        "available_time", 
        "validation_time", 
        "source"
        ]
FEED_URI = 'output/%(name)s.%(time)s.csv'
CSV_DELIMITER = '\t'
FEED_EXPORTERS = {
        'csv': '_scrapy.exporters.CsvOptionRespectingItemExporter'
        }


LOG_LEVEL = 'INFO'
LOG_FILE = 'log/%s.%s.log' % (BOT_NAME, time.strftime('%Y-%m-%d %H:%M:%S'))


ITEM_PIPELINES = {
        }


DOWNLOAD_DELAY = 3


EXTENSIONS = {
        }


CONCURRENT_REQUESTS_PER_DOMAIN = 500
CONCURRENT_REQUESTS = 1000
CLOSESPIDER_ERRORCOUNT = 50
REACTOR_THREADPOOL_MAXSIZE = 200


USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0"


