import click

import cl
from cl.log import configure_logger
from cl.main import check_cli_version, add_commands


@click.group()
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
def cli(verbose):
    """
    Russell CLI interacts with Russell server and executes your commands.
    More help is available under each command listed below.
    """
    cl.russell_host = "http://localhost:5000"
    cl.russell_web_host = "http://test.russellcloud.com"
    # cl.russell_proxy_host = "http://www.russellcloud.cn:8000"
    configure_logger(verbose)
    check_cli_version()

add_commands(cli)
