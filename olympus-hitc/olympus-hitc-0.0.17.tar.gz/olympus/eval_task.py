# coding=utf-8
from __future__ import print_function

import requests
import os
import time
import json
import sys


from utils import hitc


class Task(object):
    def __init__(self):
        super(Task, self).__init__()

    def start(self, configFile):
        res = self._do_eval(configFile)
        return res

        # task_name: "job_test_2019050702" #required
        # profile_id: "newk8s666"          #required????????????????/
        # param_ids: "D://job_test"        #required
        # images_dataset_id: "resnet-v1"   #required
        # pr_dataset_id: "TEAM-ALGORITHM-PLAT" #required
        # gt_dataset_id: 1                    #required
        # algo_task_type_id: 1                       #required
        # desc: 3  #optional
        # auth_resource_info:
        #   level:
        #   dept_id:

    # 任务执行
    def _do_eval(self, configFile):
        # ./hitc valtask submit -f configFile
        command = ["valtask", "submit", "-f %s"%configFile]  
        return hitc(command)
    

# 发起评测任务
# name: 评测任务名称
# algo_task_type_id: 算法任务类型ID
# profile_id: 评测代码包的ID
# params_ids: 评测参数的ID列表，可以设置多个
# images_dataset_id: Dataspace中dataset的ID
# gt_dataset_id: Dataspace中gt的ID
# pr_dataset_id: Dataspace中pr的ID
# dept: 模型所属的部门名称 支持 auto aiot platform
# level: 模型资源的权限级别，支持 private public
# 返回空表明创建成功，返回非空表示创建失败，返回的信息为失败原因
def start_eval(name, algo_task_type_id, profile_id, params_ids,
               images_dataset_id, gt_dataset_id, pr_dataset_id, dept, level):
    res = _do_eval(name, algo_task_type_id, profile_id, params_ids,
                   images_dataset_id, gt_dataset_id, pr_dataset_id, dept,
                   level)
    if res.get("code") != 0:
        return res.get("err_user_msg")
    return ""


def _do_eval(name, algo_task_type_id, profile_id, params_ids,
             images_dataset_id, gt_dataset_id, pr_dataset_id, dept, level):
    payload = {
        "name": name,
        "algo_task_type_id": algo_task_type_id,
        "profile_id": profile_id,
        "params_ids": params_ids,
        "images_dataset_id": images_dataset_id,
        "gt_dataset_id": gt_dataset_id,
        "pr_dataset_id": pr_dataset_id,
        "auth_info": {
            "level": level,
            "deptid": dept
        }
    }
    print(payload)
    r = requests.post("http://" + url + "/api/evaluation/v1/val-task",
                      json=payload,
                      headers={"Digest": md5, "uid": uid, "uname": uname})
    print(r)
    print(r.json())
    return r.json()
