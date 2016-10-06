#!/usr/bin/python3
# coding: utf-8
# exporters.py


from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter


class CsvOptionRespectingItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        # kwargs['delimiter'] = '\t'
        super(CsvOptionRespectingItemExporter, self).__init__(*args, **kwargs)


