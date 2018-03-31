import json
import sys

from ch.client import RussellHttpClient
from ch.log import logger


class ProjectClient(RussellHttpClient):
    """
    Client to interact with projects api
    """

    def __init__(self):
        self.url = "/projects/"
        self.project_api_url = "/{user_name}/project/{project_name}"

        super(ProjectClient, self).__init__()

    def create(self, user_name, project_name):
        response = None
        try:
            response = self.request(method="PUT",
                                    url=self.project_api_url.format(
                                        user_name=user_name,
                                        project_name=project_name)
                                    )

        except Exception as e:
            logger.error("Create remote project failed, reason: {}".format(str(e)))
        return response

    def delete(self, id):
        pass
        return True

    def get_project_name(self, id):
        project = self.request('GET',
                               url='/anonymous/project/anonymous',
                               params={'id': id})
        if isinstance(project, dict):
            return project.get('name')

    def get_project_info_by_name(self, user_name, project_name):
        project = self.request("GET",
                               url=self.project_api_url.format(user_name=user_name, project_name=project_name))
        return project

    def get_project_info_by_id(self, id):
        project = self.request('GET',
                               url='/anonymous/project/anonymous',
                               params={'id': id})
        return project
