#!/usr/bin/python3
# coding: utf-8
# items.py


from scrapy.item import Item, Field


class ProxyItem(Item):
    ip = Field(default="", type="str")
    port = Field(default="", type="int")
    protocol = Field(default="", type="str")
    anonymity = Field(default="", type="str")
    request_type = Field(default="", type="str")
    location = Field(default="", type="str")
    sp = Field(default="", type="str")
    response_delay_in_ms = Field(default="", type="int")
    available_time = Field(default="", type="str")
    validation_time = Field(default="", type="str")
    source = Field(default="", type="str")




