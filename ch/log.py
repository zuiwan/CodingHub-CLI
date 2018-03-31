# coding=utf-8

import logging

logger = logging.getLogger('cl')


def configure_logger(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(message)s', level=log_level)
