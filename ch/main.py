# coding=utf-8
import click
import ch
from ch.cli.auth import login, logout
from ch.cli.run import run
from ch.cli.fav import fav
from ch.cli.project import init
from ch.log import configure_logger
from ch.log import logger


@click.group()
@click.option('-h', '--host', default=ch.CODINGHUB_HOST, help='CodingHub server endpoint')
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
def cli(host, verbose):
    """
    Russell CLI interacts with CodingLife server and executes your commands.
    More help is available under each command listed below.
    """
    ch.CODINGHUB_HOST = host
    configure_logger(verbose)


def add_commands(cli):
    cli.add_command(init)
    cli.add_command(login)
    cli.add_command(logout)
    cli.add_command(run)
    cli.add_command(fav)


add_commands(cli)
