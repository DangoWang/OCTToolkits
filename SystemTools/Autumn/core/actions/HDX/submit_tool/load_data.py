# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/12/13
import os
import pprint
from utils import shotgun_operations


def get_task_info_by_task_dict(task_dict):
    task_id = task_dict['id'][0]
    result_dict = {}
    task_info = shotgun_operations.find_one_shotgun('Task', [['project', 'name_is', task_dict['project']],
                                                             ['id', 'is', int(task_id)]],
                                                    ['content', 'entity', 'step.Step.short_name', 'task_assignees',
                                                     'entity',  'entity.Asset.sg_hdx_asset_type', 'project',
                                                     'sg_latestversion', 'entity.Shot.episode_sg_epi_shots_episodes',
                                                     'entity.Shot.sg_scene.Scene.code'
                                                     ])
    this_user = shotgun_operations.find_one_shotgun('Group', [['sg_login', 'is', task_dict['user']]], [])
    result_dict['entity'] = task_info['entity']
    result_dict['project'] = task_dict['project']
    result_dict['project_entity'] = task_info['project']
    result_dict['task_name'] = task_info['content']
    result_dict['step'] = task_info['step.Step.short_name']
    result_dict['task_assignees'] = this_user
    result_dict['user'] = task_dict['user']
    result_dict['entity_code'] = task_info['entity']['name'] if task_info['entity'] else 'None'
    result_dict['sg_latestversion'] = task_info['sg_latestversion'] or 0
    result_dict['version'] = 'v'+str(int(result_dict['sg_latestversion'])+1).zfill(3)
    result_dict['version_number'] = str(int(result_dict['sg_latestversion'])+1)
    result_dict['entity_type'] = task_info['entity']['type'] if task_info['entity'] else 'None'
    result_dict['classify'] = task_info['entity.Asset.sg_hdx_asset_type'] or 'None'
    result_dict['sg_task'] = task_info
    result_dict['user_permission'] = shotgun_operations.get_permission(task_dict['user'])
    try:
        result_dict['episode_code'] = task_info['entity.Shot.episode_sg_epi_shots_episodes'][0]['name'] if task_info['entity.Shot.episode_sg_epi_shots_episodes'] else 'None'
        result_dict['scene_code'] = task_info['entity.Shot.sg_scene.Scene.code'] if task_info['entity.Shot.sg_scene.Scene.code'] else 'None'
    except Exception:
        result_dict['episode_code'] = 'None'
        result_dict['scene_code'] = 'None'
    return result_dict


def get_convention(project, entity_type, upload_type='Dailies'):
    convention = shotgun_operations.get_path_convention(project, entity_type, upload_type)
    return convention


def create_version(version_data):
    version_info = shotgun_operations.create_shotgun('Version', version_data)
    shotgun_operations.update_shotgun('Task', version_data['sg_task']['id'],
                                      {'sg_latestversion': version_data['sg_version_number']})
    if 'sg_path_to_movie' in version_data.keys() and os.path.isfile(version_data['sg_path_to_movie']):
        shotgun_operations.upload_shotgun('Version', version_info['id'],
                                          version_data['sg_path_to_movie'], 'sg_uploaded_movie', version_data['code'])
    return version_info



