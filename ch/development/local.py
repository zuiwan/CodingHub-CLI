import click

import ch
from ch.log import configure_logger
from ch.main import check_cli_version, add_commands


@click.group()
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
def cli(verbose):
    """
    Russell CLI interacts with Russell server and executes your commands.
    More help is available under each command listed below.
    """
    ch.russell_host = "http://localhost:5000"
    ch.russell_web_host = "http://test.russellcloud.com"
    configure_logger(verbose)
    check_cli_version()


add_commands(cli)
