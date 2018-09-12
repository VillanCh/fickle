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

        nreq = req.shift_param('e', "213")
        self.assertIsInstance(nreq.url,"https://baidu.com/a/b/c/d?e=213&a=c&zzz=123#fragment" )

if __name__ == '__main__':
    unittest.main()