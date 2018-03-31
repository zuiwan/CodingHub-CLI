import json
import sys
from ch.client import RussellHttpClient
from ch.cli.utils import get_files_in_directory, get_size
from ch.log import logger


class DataClient(RussellHttpClient):
    """
    Client to interact with Data api
    """

    def __init__(self):
        self.url = "/data/"  # Data is a subclass of modules
        super(DataClient, self).__init__()

    def create_module(self, data_module):
        request_data = data_module.to_dict()
        request_data.update({'size': get_size()})
        try:
            response = self.request("PUT",
                                    url="/module",
                                    data=json.dumps(request_data),
                                    timeout=3600)
        except Exception as e:
            sys.exit(e)
        else:
            return response

    def get(self, id):
        module_dict = self.request("GET",
                                   url="/module",
                                   params={'id': id})
        return module_dict

    def get_all(self, dataset_id):
        '''
        :return:
        '''
        response = self.request("GET",
                                url="/modules",
                                params={"module_type": "data",
                                        "entity_id": dataset_id})
        module_dicts = response.get('list', [])
        return [module_dict for module_dict in module_dicts]

    def delete(self, id):
        self.request("DELETE",
                     url="/module",
                     params={'id': id})
        return True

    def get_data_info_by_name(self, user_name, data_name):
        data = self.request("GET",
                            url="/{}/dataset/{}".format(user_name, data_name),
                            params={})
        return data

    def get_data_info_by_id(self, id):
        data = self.request("GET",
                            url="/{}/dataset/{}".format("anonymous", "anonymous"),
                            params={'id': id})
        return data
