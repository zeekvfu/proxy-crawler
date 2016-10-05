#!/usr/bin/python3
# coding: utf-8
# codec.py


# 解码
def decode(logger, content, encoding):
    if encoding is None:
        return
    try:
        return content.decode(encoding)
    except UnicodeDecodeError as e:
        logger.error("decode(): UnicodeDecodeError\t%s\t%s" % (e.encoding, e.reason))
        return


def gen_encoding_map():
    encoding_aliases = {
        'utf-8': ['utf8'],
        'gbk': ['936', 'cp936', 'ms936']
        }
    encoding_map = {}
    for encoding, aliases in encoding_aliases.items():
        for alias in aliases:
            if alias in encoding_map:
                raise ValueError('Duplicated alias in encoding_aliases!')
            encoding_map[alias] = encoding
    return encoding_map


encoding_map = gen_encoding_map()
encoding_list = ['utf-8', 'gbk', 'gb18030', 'gb2312']


