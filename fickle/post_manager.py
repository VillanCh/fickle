#!/usr/bin/env python3
# coding:utf-8
import json
from collections import OrderedDict
import warnings
from .query_manager import FickleQueryParam
from .base import FickleParam, FickleParamPosition


class FicklePostParam(FickleQueryParam):

    def __init__(self, key, value):
        FickleParam.__init__(self, key, value, FickleParamPosition.POSITION_POST)

    def __repr__(self):
        if self.value:
            return "<PostParam: {}={}>".format(self.key, self.value)
        else:
            return "<PostParam: {}>".format(self.key)


class FickleJsonParam(FickleParam):

    def __init__(self, key, value):
        FickleParam.__init__(self, key, value, FickleParamPosition.POSITION_JSON)

    @property
    def string(self):
        raise ValueError("JsonParam cannot be string.")

    def __repr__(self):
        return "<JsonParam: {}={}>".format(self.key, self.value)


class FicklePost(object):

    def __init__(self, data: str, is_json=False):
        if isinstance(data, bytes):
            data = data.decode("utf8")
        else:
            if not isinstance(data, str):
                raise ValueError("data: {} is not str.".format(data))

        self.is_json = bool(is_json)
        self.data = data
        self.params = OrderedDict()
        self.param_list = []
        self.json_object = None

        if not is_json:
            self._parse_post_to_params(data)
        else:
            self.json_object = json.loads(data)

    def _parse_post_to_params(self, query: str):
        if not query:
            return

        for block in query.split("&"):
            param = FicklePostParam.unparse_from_string(block)
            if param.key in self.params:
                warnings.warn("repeat param:{} maybe hpp?".format(param.key))
            self.params[param.key] = param
            self.param_list.append(param)

    # def _parse_json_to_params(self, query: str):
    #     self.json_object = json.loads(query)
    #     if isinstance(self.json_object, dict):
    #         FickleJsonParam()

    def shift_param(self, key, value=""):
        if self.is_json:
            if not key or not value:
                raise ValueError("json post need key and value at the same time.")
            else:
                if isinstance(self.json_object, dict):
                    new_json = json.dumps(self.json_object, key=value)
                    return json.dumps(new_json)
                else:
                    raise ValueError("json object: {} cannot be as a dict.".format(
                        self.json_object))
        else:
            if key in self.params:
                new_query_list = []
                for param in self.params.values():
                    if param.key == key:
                        new_query_list.append(
                            FicklePostParam(key, value).string
                        )
                    else:
                        new_query_list.append(param.string)

                new_query = "&".join(new_query_list)
            else:
                param = FickleQueryParam(key, value)
                if self.data:
                    new_query = "&".join((self.data, param.string))
                else:
                    new_query = param.string

        return new_query

    def json_params(self):
        if isinstance(self.json_object, dict):
            for (key, value) in self.json_object.items():
                yield FickleJsonParam(key, value)