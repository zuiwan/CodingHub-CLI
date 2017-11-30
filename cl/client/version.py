from cl.client.base import RussellHttpClient
from cl.model.version import CliVersion
from cl.log import logger as russell_logger


class VersionClient(RussellHttpClient):
    """
    Client to get API version from the server
    """
    def __init__(self):
        self.url = "/cli_version"
        super(VersionClient, self).__init__()

    def get_cli_version(self):
        data_dict = self.request("GET", self.url)
        russell_logger.debug("CLI Version info :{}".format(data_dict))
        return CliVersion.from_dict(data_dict)

