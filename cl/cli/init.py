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


# @click.option('--remote/--local', default=False, help='Init project from remote or not')
@click.command()
@click.option('--id',
              help='Remote project id to init')
@click.option('--name',
              help='Remote project name to init')
# @click.argument('project', nargs=1)
def init(id, name):
    """
    Initialize new project at the current dir.

        cl init --name test_name

    or

        cl init --id 151af60026cd462792fa5d77ef79be4d
    """
    if not id and not name:
        russell_logger.warning("Neither id or name offered\n{}".format(init.__doc__))
        return
    RussellIgnoreManager.init()
    access_token = AuthConfigManager.get_access_token()
    project_info = {}
    pc = ProjectClient()
    try:
        if id:
            project_info = pc.get_project_info_by_id(id=id)
        elif name:
            project_info = pc.get_project_info_by_name(access_token.username, name)
    except Exception as e:
        raise e
    else:
        project_id = project_info.get('id')
        name = project_info.get('name', '')
        latest_version = project_info.get('latest_version')
        if project_id:
            experiment_config = ExperimentConfig(name=name,
                                                 family_id=generate_uuid(),
                                                 project_id=project_id,
                                                 version=latest_version)
            ExperimentConfigManager.set_config(experiment_config)
            russell_logger.info("Project \"{}\" initialized in current directory".format(name))
        else:
            russell_logger.error("Project \"{}\" initialization failed in current directory".format(name))
