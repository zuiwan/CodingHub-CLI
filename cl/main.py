# coding=utf-8
import click
from distutils.version import LooseVersion
import pkg_resources
import cl
from cl.cli.auth import login, logout
from cl.cli.data import data
from cl.cli.experiment import *
from cl.cli.run import run
from cl.cli.fav import fav
from cl.cli.init import init
from cl.cli.clone import clone
from cl.client.version import VersionClient
from cl.client.service import ServiceClient
from cl.exceptions import ClException
from cl.log import configure_logger
from cl.log import logger as cl_logger

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    server_version = VersionClient().get_cli_version()
    current_version = pkg_resources.require("cl-cli")[0].version
    click.echo('Version: {}'.format(current_version))
    click.echo('Remote latest version: {}'.format(server_version.latest_version))
    if LooseVersion(current_version) < LooseVersion(server_version.min_version):
        raise ClException("""
    Your version of CLI ({}) is no longer compatible with server. Run:
        pip install -U cl-cli
    to upgrade to the latest version ({})
                """.format(current_version, server_version.latest_version))
    if LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        click.echo("""
    New version of CLI ({}) is now available. To upgrade run:
        pip install -U cl-cli
                """.format(server_version.latest_version))
    ctx.exit()

@click.group()
@click.option('-h', '--host', default=cl.russell_host, help='CodingLife server endpoint')
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="Show version info")
def cli(host, verbose):
    """
    Russell CLI interacts with CodingLife server and executes your commands.
    More help is available under each command listed below.
    """
    cl.russell_host = host
    configure_logger(verbose)
    check_cli_version()
    check_server_status()


def check_cli_version():
    """
    Check if the current cli version satisfies the server requirements
    """
    server_version = VersionClient().get_cli_version()
    current_version = pkg_resources.require("cl-cli")[0].version
    if LooseVersion(current_version) < LooseVersion(server_version.min_version):
        raise ClException("""
Your version of CLI ({}) is no longer compatible with server. Run:
    pip install -U cl-cli
to upgrade to the latest version ({})
            """.format(current_version, server_version.latest_version))
    if LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        click.echo("""
New version of CLI ({}) is now available. To upgrade run:
    pip install -U cl-cli
            """.format(server_version.latest_version))


def check_server_status():
    """
    Check if cl cloud service status now
    """
    service = ServiceClient().get_service_status()
    if service.service_status <= 0:
        raise ClException("""
            System is being maintained. Please wait until the end. 
        """)



def add_commands(cli):
    cli.add_command(data)
    cli.add_command(delete)
    cli.add_command(info)
    cli.add_command(init)
    cli.add_command(login)
    cli.add_command(logout)
    cli.add_command(logs)
    cli.add_command(output)
    cli.add_command(status)
    cli.add_command(stop)
    cli.add_command(run)
    cli.add_command(clone)
    cli.add_command(fav)


add_commands(cli)
