#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       env
   Description:
   Author:          huangzhen
   date:            2018/4/1
-------------------------------------------------
   Change Activity:
                   2018/4/1:
-------------------------------------------------
"""
__author__ = 'huangzhen'
from ch.client import RussellHttpClient
from ch.log import logger


class EnvClient(RussellHttpClient):
    """
    Client to interact with Env api
    """

    def __init__(self):
        self.url = "/env"
        super(EnvClient, self).__init__()

    def get_all(self):
        try:
            response = self.request(method="GET",
                                    url=self.url)
            return response
        except Exception as e:
            logger.info("Error while retrieving env: {}".format(str(e)))
            return {}
