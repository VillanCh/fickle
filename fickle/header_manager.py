#!/usr/bin/env python3
# coding:utf-8
import warnings
from urllib.parse import unquote
from .base import FickleParam, FickleParamPosition

class FickleCookiesParam(FickleParam):

    def __init__(self, key, value=""):
        FickleParam.__init__(self, key, value, FickleParamPosition.POSITION_COOKIES)

    @classmethod
    def unparse_from_string(cls, string: str):
        if "=" not in string:
            return cls(string)
        else:
            index = string.index("=")
            key = unquote(string[:index])
            value = unquote(string[index + 1:])
            return cls(key, value)


class FickleHeaders(object):

    def __init__(self, headers):
        self.headers = headers or {}
        self.cookies_raw = self.headers.get("Cookie", None)
        self.cookies = {}
        self._parse_cookies(self.cookies_raw)


    def _parse_cookies(self, raw: str):
        if not raw:
            return

        for block in raw.split("; "):
            param = FickleCookiesParam.unparse_from_string(block)
            if param.key in self.cookies:
                warnings.warn("repeat param:{} maybe hpp in Cookie?".format(param.key))
            self.cookies[param.key] = param

    def shift_cookies_param(self, key, value=""):
        if key in self.cookies:
            new_cookie_list = []
            for param in self.cookies.values():
                if param.key == key:
                    new_cookie_list.append(
                        FickleCookiesParam(key, value).string
                    )
                else:
                    new_cookie_list.append(param.string)
            new_cookie = "&".join(new_cookie_list)
        else:
            param = FickleCookiesParam(key, value)
            if self.cookies_raw:
                new_cookie = "; ".join((self.cookies_raw, param.string))
            else:
                new_cookie = param.string
        return dict(self.headers, Cookie=new_cookie)