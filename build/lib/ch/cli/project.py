import click
import sys
import os

import ch
from ch.client.auth import AuthClient
from ch.client.project import ProjectClient
from ch.manager.auth_config import AuthConfigManager
from ch.manager.experiment_config import ExperimentConfigManager
from ch.manager.ignore import RussellIgnoreManager
from ch.log import logger


@click.command()
@click.option('--id',
              help='Remote project id to init')
@click.option('--name',
              help='Remote project name to init')
# @click.argument('project', nargs=1)
def init(id, name):
    """
    Initialize new project at the current dir.

        russell init --name test_name

    or

        russell init --id 151af60026cd462792fa5d77ef79be4d
    """
    if not id and not name:
        logger.warning("Neither id or name offered\n{}".format(init.__doc__))
        return
    RussellIgnoreManager.init()
    try:
        pc = ProjectClient()
    except Exception as e:
        logger.error(str(e))
        return

    access_token = AuthConfigManager.get_access_token()
    project_info = {}
    try:
        if id:
            project_info = pc.get_project_info_by_id(id=id)
        elif name:
            project_info = pc.get_project_info_by_name(access_token.username, name)
    except Exception as e:
        logger.error(str(e))
        return

    else:
        if AuthClient().get_user(access_token.token).uid != project_info.get('owner_id'):
            logger.info("You can create a project then run 'russell init'")
            return
        project_id = project_info.get('id')
        name = project_info.get('name', '')
        if project_id:
            experiment_config = dict(name=name,
                                     project_id=project_id)
            ExperimentConfigManager.set_config(experiment_config)
            logger.info("Project \"{}\" initialized in current directory".format(name))
        else:
            logger.error("Project \"{}\" initialization failed in current directory".format(name))
