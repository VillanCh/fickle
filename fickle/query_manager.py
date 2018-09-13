#!/usr/bin/env python3
# coding:utf-8
import warnings
from collections import OrderedDict
from urllib.parse import urlsplit, quote, unquote, urlunsplit
from .base import FickleParam, FickleParamPosition


class FickleQueryParam(FickleParam):

    def __init__(self, key, value=""):
        FickleParam.__init__(self, key, value, FickleParamPosition.POSITION_QUERY)

    @classmethod
    def unparse_from_string(cls, string: str):
        if "=" not in string:
            return cls(string)
        else:
            index = string.index("=")
            key = unquote(string[:index])
            value = unquote(string[index + 1:])
            return cls(key, value)

    @property
    def string(self):
        if self.value:
            return super().string
        else:
            return quote(self.key)

    def __repr__(self):
        if self.value:
            return "<QueryParam: {}={}>".format(self.key, self.value)
        else:
            return "<QueryParam: {}>".format(self.key)


class FickleQuery(object):

    def __init__(self, url):
        self.url = url
        self._url_parsed = urlsplit(url)
        self.params = OrderedDict()
        self.param_list = []

        self._parse_query_to_params(self._url_parsed.query)

    def _parse_query_to_params(self, query):
        if not query:
            return

        for block in query.split("&"):
            param = FickleQueryParam.unparse_from_string(block)
            if param.key in self.params:
                warnings.warn("repeat param:{} maybe hpp?".format(param.key))
            self.params[param.key] = param
            self.param_list.append(param)

    def shift_param(self, key, value=""):
        """This method will return a tuple, containing the new url and the new query"""
        if key in self.params:
            new_query_list = []
            for param in self.params.values():
                if param.key == key:
                    new_query_list.append(
                        FickleQueryParam(key, value).string
                    )
                else:
                    new_query_list.append(param.string)

            new_query = "&".join(new_query_list)
        else:
            param = FickleQueryParam(key, value)
            if self._url_parsed.query:
                new_query = "&".join((self._url_parsed.query, param.string))
            else:
                new_query = param.string

        new_url = urlunsplit((self._url_parsed.scheme, self._url_parsed.netloc, self._url_parsed.path,
                              new_query, self._url_parsed.fragment))
        return new_url, new_query
