import json
import os

from ch.exceptions import ClException
from ch.log import logger as russell_logger


class ExperimentConfigManager(object):
    """
    Manages .russellexpt file in the current directory
    """

    CONFIG_FILE_PATH = os.path.join(os.getcwd(), ".chexpt")

    @classmethod
    def set_config(cls, experiment_config):
        russell_logger.debug("Setting {} in the file {}".format(experiment_config.to_dict(),
                                                                cls.CONFIG_FILE_PATH))
        with open(cls.CONFIG_FILE_PATH, "w") as config_file:
            config_file.write(json.dumps(experiment_config))

    @classmethod
    def get_config(cls):
        if not os.path.isfile(cls.CONFIG_FILE_PATH):
            raise ClException("Missing .chexpt file, run codehub init first")

        with open(cls.CONFIG_FILE_PATH, "r") as config_file:
            experiment_config_str = config_file.read()
        return json.loads(experiment_config_str)
