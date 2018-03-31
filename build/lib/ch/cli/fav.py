import click
import webbrowser
import traceback
from tabulate import tabulate
import sys
import ch
from ch.client.data import DataClient
from ch.client.files import FsClient, SOCKET_STATE
from ch.manager.auth_config import AuthConfigManager
from ch.manager.data_config import DataConfigManager
from ch.log import logger as cl_logger

@click.group()
def fav():
    """
    Subcommand for favorite operations
    """
    pass

@click.command()
@click.option('-r',
              default=False,
              help='Remote dataset upload status')
@click.option('-m',
              help='Message to commit',
              type=click.STRING,
              default="")
def add(ctx, r, m):
    """
    Add favorite.
    """
    pass


def print_favs(data_sources):
    headers = ["FAV ID", "CREATED", "CATEGORY", "URL", "SOURCE", "TAG"]
    data_list = []
    for data_source in data_sources:
        data_list.append([data_source.id,
                          data_source.created_pretty,
                          data_source.state,
                          data_source.size_pretty,
                          data_source.name,
                          str(data_source.version)])
    cl_logger.info(tabulate(data_list, headers=headers))

@click.command()
@click.option('-u', '--url', is_flag=True, default=False, help='Only print url for viewing data')
@click.argument('id', nargs=1)
def output(id, url):
    """
    Shows the output url of the run.
    By default opens the output page in your default browser.
    """
    # data_source = DataClient().get(id)
    data_url = "{}/files/data/{}/".format(ch.CODINGHUB_HOST, id)
    if url:
        cl_logger.info(data_url)
    else:
        cl_logger.info("Opening output directory in your browser ...")
        webbrowser.open(data_url)


@click.command()
@click.argument('id', nargs=1)
@click.option('-y', '--yes', is_flag=True, default=False, help='Skip confirmation')
def delete(id, yes):
    """
    Delete data set.
    """
    data_source = DataClient().get(id)

    if not yes:
        click.confirm('Delete Data: {}?'.format(data_source.name), abort=True, default=False)

    if DataClient().delete(id):
        cl_logger.info("Data deleted")
    else:
        cl_logger.error("Failed to delete data")

fav.add_command(delete)
fav.add_command(output)
