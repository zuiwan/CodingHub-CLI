#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       resource
   Description:
   Author:          huangzhen
   date:            2018/3/31
-------------------------------------------------
   Change Activity:
                   2018/3/31:
-------------------------------------------------
"""
__author__ = 'huangzhen'
from ch.model import BaseModel

'''
func NewResourceList(cpuType, cpuNum, gpuType, gpuNum, memType, memNum, frwType int32) *Resource_List {
    return &Resource_List{
        Cpu: CPU_FLAG | cpuType | cpuNum,
        Mem: MEM_FLAG | memType | memNum,
        Gpu: GPU_FLAG | gpuType | gpuNum,
        Frw: FRW_FLAG | frwType,
    }
}
'''


class Resources(BaseModel):
    def __init__(self, cpuType, cpuNum, gpuType, gpuNum, memType, memNum, frwType):
        self.cpu_type = cpuType
        self.cpu_num = cpuNum
        self.gpu_type = gpuType
        self.gpu_num = gpuNum
        self.mem_type = memType
        self.mem_num = memNum
        self.frw_type = frwType