# coding=utf-8

from pytz import timezone
from tzlocal import get_localzone

PST_TIMEZONE = timezone("Asia/Shanghai")
LOCAL_TIMEZONE = get_localzone()

DEFAULT_FILE_IGNORE_LIST = """
# Directories to ignore when uploading code to cl
# Do not add a trailing slash for directories
.*
.git
.eggs
eggs
lib
lib64
parts
sdist
var
"""
