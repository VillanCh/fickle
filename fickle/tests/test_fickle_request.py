#!/usr/bin/env python3
# coding:utf-8
import unittest
from .. import core

class FickleReqTestCase(unittest.TestCase):
    
    def test_urcase(self):
        url = "https://baidu.com/a/b/c/d?e=f&a=c&zzz=123#fragment"
        req = core.FickleRequest.build(url, "GET", "")
        self.assertIsInstance(req, core.FickleRequest)

    def test_fickle_request(self):
        url = "https://baidu.com/a/b/c/d?e=f&a=c&zzz=123#fragment"
        req = core.FickleRequest.build(url)

        nreq = req.shift_query_param('e', "213")
        self.assertEqual(nreq.url,"https://baidu.com/a/b/c/d?e=213&a=c&zzz=123#fragment" )

        _ = req.shift_post_param("e", "213")
        self.assertEqual(_.data, "e=213")

        req = core.FickleRequest.build(url='https://baidu.com')
        nreq = req.shift_query_param("test", "value")
        self.assertEqual(nreq.url, "https://baidu.com/?test=value")

        req = core.FickleRequest.build(method="POST", url='http://baidu.com/', data="test=234&te=1")
        nreq = req.shift_post_param("test", "123")
        self.assertEqual(nreq.data, "test=123&te=1")

        nreq = req.shift_cookies_param("test", "value")
        self.assertEqual(nreq.headers['Cookie'], "test=value")

        preq = nreq.prepare()
        req = core.FickleRequest.from_request(preq)
        nreq = req.shift_cookies_param("key", "value2")
        self.assertEqual(nreq.headers["Cookie"], "test=value; key=value2")

        nreq = req.shift_cookies_param("test", "aaa")
        self.assertEqual(nreq.headers["Cookie"], "test=aaa")

if __name__ == '__main__':
    unittest.main()