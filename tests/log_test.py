import sys
from time import sleep

def long_task():
    if sys.version > '3':
        big = sys.maxsize
    else:
        big = sys.maxint
    while big:
        sleep(1)
        big -= 1


long_task()