import click
import traceback
import webbrowser
from tabulate import tabulate
from time import sleep
import sys

import cl
from cl.cli.utils import get_task_url, get_module_task_instance_id
from cl.client.common import get_url_contents
from cl.client.experiment import ExperimentClient
from cl.client.module import ModuleClient
from cl.client.task_instance import TaskInstanceClient
from cl.client.project import ProjectClient
from cl.config import generate_uuid
from cl.manager.auth_config import AuthConfigManager
from cl.manager.experiment_config import ExperimentConfigManager
from cl.manager.cl_ignore import RussellIgnoreManager
from cl.model.experiment_config import ExperimentConfig
from cl.log import logger as russell_logger
from cl.exceptions import *

@click.command()
@click.argument('project_url_or_id', nargs=1)
def clone(project_url_or_id):
    """
    Clone remote project at the current dir.
    """
    # experiment_config = ExperimentConfig(name=project,
                                         # family_id=generate_uuid())
    # ExperimentConfigManager.set_config(experiment_config)
    # RussellIgnoreManager.init()

    ProjectClient().clone(project_url_or_id,
                          uncompress=True,
                          delete_after_uncompress=True)


@click.command()
@click.argument('project_url_or_id', nargs=1)
def clone2(project_url_or_id):
    """
    For Development: Clone remote project at the current dir.
    """
    client = ProjectClient()
    try:
        project_name = str(client.get_project_name(project_url_or_id))
        russell_logger.debug(project_name)
        if not project_name or not isinstance(project_name, str) or not len(project_name) > 0:
            sys.exit("Project id is illegal or not found")
        else:
            url = client.url + 'clone/' + project_url_or_id
            for status in client.async_request_clone(url=url, api_version=2):
                if isinstance(status, dict):
                    if 'task_id' in status:
                        try:
                            client.download_compressed(url + "?task_id={}&stream=1".format(status.get('task_id')),
                                                   compression='zip',
                                                   uncompress=True,
                                                   delete_after_uncompress=True,
                                                   dir=project_name,
                                                   api_version=2)
                        except Exception as e:
                            russell_logger.error("Clone ERROR! {}".format(e))
                    else:
                        num = status.get('num')
                        size = status.get('size')
                        russell_logger.info("remote: " + str(num) + " files compressed")
                else:
                    russell_logger.error("Clone ERROR! {}".format("Please retry"))

    except Exception as e:
        russell_logger.error("Clone ERROR! {}".format(e))