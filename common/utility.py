#!/usr/bin/python3
# coding: utf-8
# utility.py


import os
import random
import logging
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


# 将两个 list 合并起来，并且保持原来元素的相对顺序
def merge_list_preserving_order(l1, l2):
    return list(OrderedDict.fromkeys(l1 + l2))


def get_logger(log_file):
    _format = '%(asctime)s %(process)d %(thread)d %(levelname)s | %(message)s'
    formatter = logging.Formatter(_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(log_file)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    print(__file__)
    print(os.path.realpath(__file__))
    print(get_script_dir())


