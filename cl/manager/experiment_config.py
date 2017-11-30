import json
import os

from cl.exceptions import ClException
from cl.model.experiment_config import ExperimentConfig
from cl.log import logger as russell_logger


class ExperimentConfigManager(object):
    """
    Manages .russellexpt file in the current directory
    """

    CONFIG_FILE_PATH = os.path.join(os.getcwd() + "/.clexpt")

    @classmethod
    def set_config(cls, experiment_config):
        russell_logger.debug("Setting {} in the file {}".format(experiment_config.to_dict(),
                                                              cls.CONFIG_FILE_PATH))
        with open(cls.CONFIG_FILE_PATH, "w") as config_file:
            config_file.write(json.dumps(experiment_config.to_dict()))

    @classmethod
    def get_config(cls):
        if not os.path.isfile(cls.CONFIG_FILE_PATH):
            raise ClException("Missing .clexpt file, run cl init first")

        with open(cls.CONFIG_FILE_PATH, "r") as config_file:
            experiment_config_str = config_file.read()
        return ExperimentConfig.from_dict(json.loads(experiment_config_str))
