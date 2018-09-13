#!/usr/bin/env python3
# coding:utf-8
from urllib.parse import quote

class FickleParamPosition:
    POSITION_QUERY = 'query'
    POSITION_POST = 'post'
    POSITION_JSON = 'json'
    POSITION_COOKIES = 'cookies'
    POSITION_HEADER = 'header'

    POSITIONS = [
        POSITION_POST, POSITION_QUERY, POSITION_COOKIES,
        POSITION_HEADER, POSITION_JSON
    ]


class FickleParam(object):

    def __init__(self, key, value, position):
        if position not in FickleParamPosition.POSITIONS:
            raise ValueError("position: {} in not existed in {}".format(
                position, FickleParamPosition.POSITIONS
            ))

        if not isinstance(key, str):
            raise ValueError("key: {} is not a str but {}".format(
                key, type(key)
            ))

        if not isinstance(value, str):
            raise ValueError("value: {} is not a str but {}".format(
                value, type(value)
            ))

        self.key = key
        self.value = value
        self.position = position

    @property
    def string(self):
        return "{}={}".format(quote(self.key),quote(self.value))