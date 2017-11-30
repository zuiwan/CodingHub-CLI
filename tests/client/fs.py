import sys
sys.path.append(".")
sys.path.append("..")
from cl.client.files import FsClient
#139.224.114.10:9200
import progressbar
from enum import Enum

try:
    import _thread
except ImportError:
    import thread as _thread
import shutil
import websocket
from cl.client.base import RussellHttpClient
from cl.cli.utils import *
from cl.log import logger as russell_logger
from cl.exceptions import *
if __name__ == '__main__':
    # FsClient().socket_upload('dataset',
    #               './',
    #               'afasdfa',
    #               '12313120',
    #               'yuanxingchi',
    #               'example')
    fc = FsClient()
    # FsClient().socket_upload(file_type="data",
    #                          filename="./",
    #                          access_token="token",
    #                          file_id="123456",
    #                          user_name="hz",
    #                          data_name="example")
    def on_error(error):
        print str(error)
    def on_msg(ws, msg):
        print msg
    def on_close(ws):
        print ws, dir(ws)
    def on_open(ws):
        print ws
    web_socket = websocket.WebSocketApp(
        url="ws://test.fs.russellcloud.com:8081/data/123456/",
        header={

        },
        on_message=on_msg,
        on_error=on_error,
        on_close=on_close
    )
    web_socket.on_open = on_open
    web_socket.run_forever()
    print("test success")