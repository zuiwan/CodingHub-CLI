# coding: utf-8
from __future__ import print_function

import shutil
import click
import sys
from checksumdir import dirhash

try:
    from pipes import quote as shell_quote
except ImportError:
    from shlex import quote as shell_quote
from tabulate import tabulate
from time import sleep
from ch.cli.utils import (wait_for_url, get_files_in_current_directory, sizeof_fmt, copy_files)
from ch.client.env import EnvClient
from ch.client.job import ExperimentClient
from ch.client.project import ProjectClient
from ch.manager.auth_config import AuthConfigManager
from ch.manager.experiment_config import ExperimentConfigManager
from ch.model.job import JobReq, JobSpecification
from ch.log import logger as logger
import webbrowser

_TEMP_DIR = ".codinghubTemp"


@click.command()
@click.option('--data',
              multiple=True,
              help='Data source id(s) to use')
@click.option('--jupyter/--no-jupyter',
              help='Open jupyter mode',
              default=False)
@click.option('--resubmit/--no-resubmit',
              help='Resubmit job request (will not create new job, generally after the last submit is rejected)',
              default=False)
@click.option('--eager/--no-eager',
              help='Run instantly(as soon as fast)',
              default=False)
@click.option('--value',
              type=click.FLOAT,
              help='Bidding price(￥Yuan) for this run')
@click.option('--duration',
              type=click.STRING,
              help='Estimated total duration of this run, format like "7d5h10m2s" in golang')
@click.option('--earliest',
              type=str,
              help='The beginning of time window for this run')
@click.option('--deadline',
              type=str,
              help='The deadline of time window for this run')
@click.option('--tensorboard/--no-tensorboard',
              help='Open tensorboard service',
              default=False)
@click.option('--env',
              help='Deep learning framework environment type to use')
@click.option('--os',
              help="Operating System to use")
@click.option('-gt', '--gputype',
              help="GPU type to use")
@click.option('-gn', '--gpunum',
              help="GPU card num to use")
@click.option('-ct', '--cputype',
              help="CPU type to use")
@click.option('-cn', '--cpunum',
              help='CPU core num to use')
@click.option('-mt', '--memtype',
              help="Memory type to use")
@click.option('-mn', '--memnum',
              help='Memory GB num to use')
@click.option('--message', '-m',
              help='Message to commit',
              type=click.STRING,
              default="")
@click.option('--version', '-v',
              help='Code Version to run',
              type=click.INT)
# @click.option('--tensorboard/--no-tensorboard',
#               help='Run tensorboard')
@click.argument('command', nargs=-1)
def run(resubmit, command, env, jupyter, tensorboard, data, version, message, os, cputype, cpunum, gputype, gpunum,
        memtype, memnum, eager, value, earliest, deadline, duration):
    '''

    :param resubmit:
    :param command:
    :param env:
    :param jupyter:
    :param tensorboard:
    :param data:
    :param version:
    :param message:
    :param os:
    :param cputype:
    :param cpunum:
    :param gputype:
    :param gpunum:
    :param memtype:
    :param memnum:
    :param eager:
    :param value:
    :param earliest:
    :param deadline:
    :param duration:
    :return:
    '''
    """
    """
    # 初始化客户端
    try:
        ec = ExperimentClient()
    except Exception as e:
        logger.error(str(e))
        return
    if resubmit is True:
        # 只关注竞价部分的参数
        jobSpec = {}  # 从本地配置文件或者服务器读取上次竞价失败的（或者本地配置文件中的，上次竞价成功的也行）作业详情
        jobId = jobSpec["id"]
        # 提交作业请求
        jobReq = JobReq(duration=duration, tw_end=deadline, tw_start=earliest, job_id=jobId, value=value,
                        resources=jobSpec["resources"])
        resp = ec.submit(jobId, jobReq)
        if resp["accepted"] == False:
            logger.info("This job submit is not accepted, reason: {}".format(resp["message"]))
            return
    # 检查备注信息长度
    if message and len(message) > 1024:
        logger.error("Message body length over limit")
        return

    # 获取认证令牌
    access_token = AuthConfigManager.get_access_token()
    # 读取本地作业配置信息
    experiment_config = ExperimentConfigManager.get_config()

    # 组装命令成列表
    command_str = ' '.join(command)
    # # 处理挂载数据集
    # success, data_ids = process_data_ids(data)
    # if not success:
    #     return

    # 处理深度学习框架配置
    if not env:
        # 未指定，获取作业所属项目的默认框架作为此次作业的框架
        env = ProjectClient().get_project_info_by_id(experiment_config["project_id"]).get('default_env')

    # 检查所有资源的组合是否合法
    if not validate_resource_list(env, jupyter, tensorboard, os, cputype, cpunum, gputype, gpunum):
        return

    # 上传代码到云端或者指定云端代码
    # # 如果指定了代码版本
    # if version:
    #     module_resp = ModuleClient().get_by_entity_id_version(experiment_config.project_id, version)
    #     if not module_resp:
    #         logger.error("Remote project does not existed")
    #         return
    #     module_id = module_resp.get('id')
    # else:
    #     # Gen temp dir
    #     try:
    #         # upload_files, total_file_size_fmt, total_file_size = get_files_in_directory('.', 'code')
    #         # save_dir(upload_files, _TEMP_DIR)
    #         file_count, size = get_files_in_current_directory('code')
    #         if size > 100 * 1024 * 1024:
    #             sys.exit("Total size: {}. "
    #                      "Code size too large to sync, please keep it under 100MB."
    #                      "If you have data files in the current directory, please upload them "
    #                      "separately using \"russell data\" command and remove them from here.\n".format(
    #                 sizeof_fmt(size)))
    #         copy_files('.', _TEMP_DIR)
    #     except OSError:
    #         sys.exit("Directory contains too many files to upload. Add unused directories to .russellignore file.")
    #         # logger.info("Creating project run. Total upload size: {}".format(total_file_size_fmt))
    #         # logger.debug("Creating module. Uploading: {} files".format(len(upload_files)))
    #
    #     hash_code = dirhash(_TEMP_DIR)
    #     logger.debug("Checking MD5 ...")
    #     module_resp = ModuleClient().get_by_codehash_entity_id(hash_code, experiment_config.project_id)
    #     if module_resp:  # if code same with older version, use existed, don`t need upload
    #         module_id = module_resp.get('id')
    #         version = module_resp.get('version')
    #         logger.info("Use older version-{}.".format(version))
    #     else:
    #         version = experiment_config.version
    #         # Create module
    #         module = Module(name=experiment_config.name,
    #                         description=message,
    #                         family_id=experiment_config.family_id,
    #                         version=version,
    #                         module_type="code",
    #                         entity_id=experiment_config.project_id
    #                         )
    #         module_resp = mc.create(module)
    #         if not module_resp:
    #             logger.error("Remote project does not existed")
    #             return
    #         version = module_resp.get('version')
    #         experiment_config.set_version(version=version)
    #         ExperimentConfigManager.set_config(experiment_config)
    #
    #         module_id = module_resp.get('id')
    #         project_id = module_resp.get('entity_id')
    #         if not project_id == experiment_config.project_id:
    #             logger.error("Project conflict")
    #
    #         logger.debug("Created module with id : {}".format(module_id))
    #
    #         # Upload code to fs
    #         logger.info("Syncing code ...")
    #         fc = FsClient()
    #         try:
    #             fc.socket_upload(file_type="code",
    #                              filename=_TEMP_DIR,
    #                              access_token=access_token.token,
    #                              file_id=module_id,
    #                              user_name=access_token.username,
    #                              data_name=experiment_config.name)
    #         except Exception as e:
    #             shutil.rmtree(_TEMP_DIR)
    #             logger.error("Upload failed: {}".format(str(e)))
    #             return
    #         else:
    #             ### check socket state, some errors like file-server down, cannot be catched by `except`
    #             state = fc.get_state()
    #             if state == SOCKET_STATE.FAILED:
    #                 logger.error("Upload failed, please try after a while...")
    #                 return
    #         finally:
    #             try:
    #                 shutil.rmtree(fc.temp_dir)
    #             except FileNotFoundError:
    #                 pass
    #
    #         ModuleClient().update_codehash(module_id, hash_code)
    #         logger.info("\nUpload finished")
    #
    #     # rm temp dir
    #     shutil.rmtree(_TEMP_DIR)
    #     logger.debug("Created code with id : {}".format(module_id))

    # 创建作业描述指标
    jobSpecification = JobSpecification(message=message, code_id="", data_ids=[],
                                        command=command_str,
                                        project_id=experiment_config["project_id"],
                                        framework=env,
                                        enable_jupyter=jupyter,
                                        enable_tensorboard=tensorboard,
                                        os="ubuntu:16",
                                        gpunum=gpunum,
                                        gputype=gputype,
                                        cpunum=cpunum,
                                        cputype=cputype,
                                        memnum=memnum,
                                        memtype=memtype)
    # 提交该作业描述，由服务器保存
    jobId = ec.create(jobSpecification)
    logger.debug("Created job specification : {}".format(jobId))

    # # 更新本地作业配置
    # experiment_config.set_experiment_predecessor(experiment_id)
    # ExperimentConfigManager.set_config(experiment_config)

    # 打印作业描述信息
    experiment_name = "{}/{}:{}".format(access_token.username,
                                        experiment_config["project_id"],
                                        version)

    table_output = [["JOB ID", "NAME", "VERSION"],
                    [jobId, experiment_name, version]]
    logger.info(tabulate(table_output, headers="firstrow"))
    logger.info("")

    # 提交作业请求
    jobReq = JobReq(duration=duration, tw_end=deadline, tw_start=earliest, job_id=jobId, value=value,
                    resources=jobSpecification.resources)
    resp = ec.submit(jobId, jobReq)
    if resp["accepted"] == False:
        logger.info("This job submit is not accepted, reason: {}".format(resp["message"]))
        return

    # 作业成功提交后，处理jupyter/tensorboard
    task_url = {}
    if jupyter is True:
        while True:
            # Wait for the experiment / task instances to become available
            try:
                experiment = ec.get(jobId)
                if experiment.state != "waiting" and experiment.task_instances:
                    break
            except Exception as e:
                logger.debug("Experiment not available yet: {}".format(jobId))

            logger.debug("Experiment not available yet: {}".format(jobId))
            sleep(1)
            continue

        task_url = ec.get_task_url(jobId)
        jupyter_url = task_url["jupyter_url"]
        print("Setting up your instance and waiting for Jupyter notebook to become available ...")
        if wait_for_url(jupyter_url, sleep_duration_seconds=2, iterations=900):
            logger.info("\nPath to jupyter notebook: {}".format(jupyter_url))
            webbrowser.open(jupyter_url)
        else:
            logger.info("\nPath to jupyter notebook: {}".format(jupyter_url))
            logger.info(
                "Notebook is still loading or can not be connected now. View logs to track progress")

    if tensorboard is True:
        if not task_url.get("tensorboard_url"):
            task_url = ec.get_task_url(jobId)
        tensorboard_url = task_url["tensorboard_url"]
        logger.info("\nPath to tensorboard: {}".format(tensorboard_url))

    logger.info("""
        To view logs enter:
            ch logs {}
                """.format(jobId))


def validate_resource_list(env, jupyter, tensorboard, os, cputype, cpunum, gputype, gpunum):
    # TODO
    return True


def process_data_ids(data):
    # TODO
    if len(data) > 5:
        logger.error(
            "Cannot attach more than 5 datasets to a task")
        return False, None
    # Get the data entity from the server to:
    # 1. Confirm that the data id or uri exists and has the right permissions
    # 2. If uri is used, get the id of the dataset
    data_ids = []
    mc = DataClient()
    for data_id_and_path in data:
        if ':' in data_id_and_path:
            data_id, path = data_id_and_path.split(':')
        else:
            data_id = data_id_and_path
            path = None
        data_obj = mc.get(data_id)
        if not data_obj:
            logger.error("Data not found by id: {}".format(data_id))
            return False, None
        else:
            if path is None:
                path = "{}-{}".format(data_obj.name, data_obj.version)
            data_ids.append("{id}:{path}".format(id=data_obj.id, path=path))

    return True, data_ids
