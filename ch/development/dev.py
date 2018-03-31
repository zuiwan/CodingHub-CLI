# coding=utf-8
import click

from ch.main import check_cli_version, add_commands, print_version

from ch.log import configure_logger

import ch


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
    ch.russell_host = "http://api.cannot.cc"
    ch.russell_web_host = "http://web.cannot.cc"
    ch.russell_fs_host = "fs.cannot.cc"
    ch.russell_fs_port = 8081
    configure_logger(verbose)


add_commands(cli)
