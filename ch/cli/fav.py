import click
import webbrowser
import traceback
from tabulate import tabulate
import sys
import cl
from cl.client.data import DataClient
from cl.client.files import FsClient, SOCKET_STATE
from cl.client.module import ModuleClient
from cl.manager.auth_config import AuthConfigManager
from cl.manager.data_config import DataConfigManager
from cl.model.module import *
from cl.log import logger as cl_logger

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
    if m and len(m) > 1024:
        cl_logger.error("Message body length over limit")
        sys.exit()
    message = m
    try:
        data_config = DataConfigManager.get_config()
        access_token = AuthConfigManager.get_access_token()
    except Exception as e:
        cl_logger.error("Configuration Error")
        return

    # version = data_config.version + 1
    version = data_config.version

    # Create data object

    data = ModuleRequest(name=data_config.name,
                         description=message,
                         module_type="data",
                         entity_id=data_config.dataset_id,
                         version=version)

    dc = DataClient()
    if r:
        module_info = ModuleClient().get(id=data_config.data_predecessor)
        print_upload([module_info])
        return

    create_module_info = dc.create_module(data)
    data_module_id = create_module_info.get('id')
    data_module_version = int(create_module_info.get('version'))

    # Update expt config including predecessor
    data_config.set_version(data_module_version)
    data_config.set_data_predecessor(data_module_id)
    DataConfigManager.set_config(data_config)

    fc = FsClient()
    try:
        fc.socket_upload(file_type="data",
                         filename="./",
                         access_token=access_token.token,
                         file_id=data_module_id,
                         user_name=access_token.username,
                         data_name=data_config.name)
    except Exception as e:
        sys.exit(e)

    cl_logger.debug("Created data with id : {}".format(data_module_id))
    cl_logger.info("\nUpload finished")

    data_name = "{}/{}:{}".format(access_token.username,
                                  data_config.name,
                                  data_module_version)
    # Print output
    table_output = [["DATA ID", "NAME", "VERSION"],
                    [data_module_id, data_name.encode("utf-8"), data_module_version]]
    cl_logger.info(tabulate(table_output, headers="firstrow"))
    cl_logger.info('''
Upload finished, start extracting to data module\n
    To check data status enter:
        cl data status {}\n'''.format(data_module_id))

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
    data_url = "{}/files/data/{}/".format(cl.russell_host, id)
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
