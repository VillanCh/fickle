#!/usr/bin/env python3
# coding:utf-8
import requests
from .query_manager import FickleQuery

class FickleRequest(object):

    def __init__(self, prepared_request: requests.PreparedRequest):
        self.prepared_request = prepared_request
        self.fickle_query = FickleQuery(self.prepared_request.url)

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

    def shift_param(self, key, value):
        url = fickle_query.shift_param()
        req = self._new_request(url=url)
        