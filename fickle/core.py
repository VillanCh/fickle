#!/usr/bin/env python3
# coding:utf-8
import requests
from .query_manager import FickleQuery
from .post_manager import FicklePost
from .header_manager import FickleHeaders

class FickleRequest(object):

    def __init__(self, prepared_request: requests.PreparedRequest):
        self.prepared_request = prepared_request

        # parse query
        self.fickle_query = FickleQuery(self.prepared_request.url)

        # parse post data
        _json = 'application/json' == self.prepared_request.headers.get("Content-Type")
        self.fickle_post = FicklePost(prepared_request.body or "", _json)

        # parse headers
        self.fickle_headers = FickleHeaders(prepared_request.headers or {})

    @classmethod
    def build(cls, url, method="GET", query=None, data=None, auth=None, headers=None, cookies=None):
        req = requests.Request(method, url, headers, None, data, query, auth, cookies)
        return cls.from_request(req)

    @classmethod
    def from_request(cls, request):
        if isinstance(request, requests.Request):
            request = request.prepare()

        if isinstance(request, requests.PreparedRequest):
            return cls(request)

        raise ValueError("request: {} is not a requests.PreparedRequest.")

    def _new_request(self, url=None, method=None, headers=None, body=None):
        url = url or self.prepared_request.url
        method = method or self.prepared_request.method
        headers = headers or self.prepared_request.headers
        body = body or self.prepared_request.body
        return requests.Request(method, url, headers, None, body, None, None, None)

    def shift_query_param(self, key, value=""):
        url, _ = self.fickle_query.shift_param(key, value)
        req = self._new_request(url=url)
        return req

    def shift_post_param(self, key, value=""):
        data = self.fickle_post.shift_param(key, value)
        req = self._new_request(body=data)
        return req

    def shift_cookies_param(self, key, value):
        headers = self.fickle_headers.shift_cookies_param(key, value)
        req = self._new_request(headers=headers)
        return req

    def params(self):
        for param in self.fickle_query.params.values():
            yield param

        if self.fickle_post.is_json:
            for param in self.fickle_post.json_params():
                yield param
        else:
            for param in self.fickle_post.params.values():
                yield param
