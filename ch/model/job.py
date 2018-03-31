from marshmallow import Schema, fields, post_load
from ch.model import BaseModel


class JobReqSchema(Schema):
    duration = fields.Int()
    tw_start = fields.Time()
    tw_end = fields.Time()
    job_id = fields.Str()
    value = fields.Int()
    resources = fields.Dict()

    @post_load
    def make_jobreq(self, data):
        return JobReq(**data)


class JobReq(BaseModel):
    schema = JobReqSchema(strict=True)

    def __init__(self, duration, tw_start, tw_end, job_id, value, resources):
        self.id = id
        self.duration = duration
        self.tw_start = tw_start
        self.tw_end = tw_end
        self.job_id = job_id
        self.value = value
        self.resources = resources


class JobSchema(Schema):

    @post_load
    def make_job(self, data):
        return JobSpecification(**data)


'''
注：有些数据应由服务端生成
type Job struct {
    Id ID `json:"id"`
    // 实际运行时长
    Duration time.Duration `json:"duration"`
    // 创建和修改时间
    TCreated  time.Time `json:"t_created"`
    TModified time.Time `json:"t_modified"`

    // 归属于项目
    ProjectId ID `json:"project_id"`

    // 代码文件
    CodeId ID `json:"code_id"`
    // 数据文件
    DataIds Data_Ids_T `json:"data_id"`

    //// 运行环境
    Env *Environment `json:"env"`

    // 启动后的容器入口命令
    EntryCmd string `json:"entry_cmd"`
    // CLI启动命令
    StartCmd string `json:"start_cmd"`

    // 是否开启xx模式
    BTensorboard bool `json:"b_tensorboard"`
    BJupyter     bool `json:"b_jupyter"`

    // （是否）已启动/结束（时间）
    TStarted time.Time `json:"t_started"`
    TEnded   time.Time `json:"t_ended"`

    // 所属用户ID
    UId ID `json:"u_id"`
    // 所属团队ID
    GId ID `json:"g_id"`
    // 权限
    Perm int8 `json:"perm"`
    // 用户描述
    Doc string `json:"doc"`
}
'''


class JobSpecification(BaseModel):
    def __init__(self, project_id, code_id, data_ids, enable_tensorboard, enable_jupyter, message, command,
                 os, gputype, gpunum, cputype, cpunum, memtype, memnum, framework):
        self.project_id = project_id
        self.code_id = code_id
        self.data_ids = data_ids
        self.b_tensorboard = enable_tensorboard
        self.b_jupyter = enable_jupyter
        self.doc = message
        self.entry_cmd = command
        self.os = os
        self.framework = framework
        self.gputype = gputype
        self.gpunum = gpunum
        self.cputype = cputype
        self.cpunum = cpunum
        self.memtype = memtype
        self.memnum = memnum

    @property
    def resources(self):
        return {
            "gpu_type": self.gputype,
            "gpu_num": self.gpunum,
            "cpu_type": self.cputype,
            "cpu_num": self.cpunum,
            "mem_type": self.memtype,
            "mem_num": self.memnum,
            "frw_type": self.env
        }
