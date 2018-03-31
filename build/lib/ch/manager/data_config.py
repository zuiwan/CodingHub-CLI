import json
import os
from ch.exceptions import ClException
from ch.log import logger as logger


class DataConfigManager(object):
    """
    Manages .russelldata file in the current directory
    """

    CONFIG_FILE_PATH = os.path.join(os.getcwd(), ".chdata")

    @classmethod
    def set_config(cls, data_config):
        logger.debug("Setting {} in the file {}".format(data_config.to_dict(),
                                                        cls.CONFIG_FILE_PATH))
        with open(cls.CONFIG_FILE_PATH, "w") as config_file:
            config_file.write(json.dumps(data_config.to_dict()))

    @classmethod
    def get_config(cls):
        if not os.path.isfile(cls.CONFIG_FILE_PATH):
            raise ClException("Missing .cldata file, run ch data init first")

        with open(cls.CONFIG_FILE_PATH, "r") as config_file:
            data_config_str = config_file.read()
        return json.loads(data_config_str)
