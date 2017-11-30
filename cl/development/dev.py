# coding=utf-8
import click

import cl
from cl.log import configure_logger
from cl.main import check_cli_version, add_commands, print_version

from cl.cli.experiment import log
from cl.cli.project import clone2
from cl.cli.data import *
from cl.cli.data import _upload
from cl.log import configure_logger

# is_eager=True 表明该命令行选项优先级高于其他选项；
# expose_value=False 表示如果没有输入该命令行选项，会执行既定的命令行流程；
# callback 指定了输入该命令行选项时，要跳转执行的函数；

@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="Show version info")
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
def cli(verbose):
    """
    Russell CLI interacts with Russell server and executes your commands.
    More help is available under each command listed below.
    """
    cl.russell_host = "http://test.dl.russellcloud.com"
    cl.russell_web_host = "http://test.russellcloud.com"
    cl.russell_proxy_host = "https://dev.russellcloud.com:8000"
    cl.russell_fs_host = "test.fs.russellcloud.com"
    cl.russell_fs_port = 8081
    configure_logger(verbose)

add_commands(cli)

data.add_command(_upload)
cli.add_command(clone2)
cli.add_command(data)
cli.add_command(log)
