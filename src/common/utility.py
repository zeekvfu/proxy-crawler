#!/usr/bin/python3
# coding: utf-8
# utility.py


import os
import json
import random
import logging
import itertools

from collections import OrderedDict


# 获取脚本所在的路径
def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


# 从 sequence 中随机获取一个元素
# use `random.choice()` instead
def random_elem(l):
    if l is None or len(l) == 0:
        return
    index = random.randint(0, len(l)-1)
    return l[index]


def empty_str_to_none(s):
    if s is not None and len(s) == 0:
        s = None
    return s


# 与 str() 方法的区别是，可以自定义将 None 转化成什么 str
def obj_to_str(obj, none_to_what='null'):
    if obj is None:
        obj = none_to_what
    return str(obj)


# faltten a list
def flatten_list(l):
    return [ item for sublist in l for item in sublist ]


# 将 list 合并起来，并且保持相对顺序（list 间相对顺序 + list 内元素相对顺序）
def merge_list_preserving_order(*args):
    result = itertools.chain(*args)
    return list(OrderedDict.fromkeys(result))


def get_logger(log_file, log_level=logging.DEBUG):
    _format = '%(asctime)s %(process)d %(thread)d %(levelname)s | %(message)s'
    formatter = logging.Formatter(_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(log_file)
    logger.addHandler(file_handler)
    if isinstance(log_level, str):
        log_level = eval(log_level)
    logger.setLevel(log_level)
    return logger


if __name__ == '__main__':
    print(__file__)
    print(os.path.realpath(__file__))
    print(get_script_dir())


