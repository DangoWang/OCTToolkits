#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
import datetime
import os
import pprint
import shotgun_api3
from dayu_widgets.qt import *
from operator import methodcaller
import common_methods
import Queue
# from oct_rpc import client


class SGOperationThread(QThread):

    def __init__(self):
        super(SGOperationThread, self).__init__()
        self.mode = None
        self.data = None
        self.data_queue = Queue.Queue()
        self.__sg = shotgun_api3.Shotgun("http://sg.ds.com",
                                         script_name="octlauncher",
                                         ensure_ascii=False,
                                         api_key="hfda$dlcpzgPugqas4tlogdcc")
        # self.__sg = client.OCT_RPC_CLIENT(host="sg.ds.com", port=9090)
        # self.__sg = shotgun_api3.Shotgun("http://sg.octmedia.com:8000",  # http_proxy="139.129.207.13:3128",
        #                                  login="td-sg", ensure_ascii=False, password="octmedia-2019")

    def run(self, *args, **kwargs):
        if self.data:
            try:
                final_result = methodcaller(self.mode, *self.data)(self.__sg)
                # final_result = self.__sg.call_sg(self.mode, self.data) or []
                self.data_queue.put(final_result)
            except Exception, e:
                print u'执行%s出现错误.%s' % (self.mode, self.data), e


@common_methods.func_cache(maxsize=10, memory_time=3)
def __sg_operate_doit(mode, data, sg_instance=False):
    # global operate_thread
    if not sg_instance:
        operate_thread = SGOperationThread()
    else:
        operate_thread = sg_instance
    operate_thread.mode = mode
    operate_thread.data = data
    operate_thread.start()
    operate_thread.wait()
    while not operate_thread.data_queue.empty():
        result = operate_thread.data_queue.get()
        return result
    return None


def get_project():
    return u"DSF"
    # return os.environ.get('oct_project').encode('utf-8').decode('unicode_escape')


def get_user():
    return u'TD_Group'
    # return os.environ.get('oct_user').encode('utf-8').decode('unicode_escape')


def get_step(user, sg_instance=False):
    steps = find_one_shotgun('Group', [['sg_login', 'is', user]], ['sg_step'], sg_instance=sg_instance)
    if steps:
        # return steps
        return [n['name'] for n in steps['sg_step']]


def get_envision(environ_name):
    # return u'TD_Group'
    return os.environ.get(environ_name)


def get_tasks(project_name, user, sg_instance=False):
    filters = [['project', 'name_is', project_name], ['task_assignees.Group.sg_login', 'is', user]]
    fields = ['content', 'step', 'step.Step.short_name', 'step.Step.code', 'entity.Asset.code', 'entity.Asset.sg_asset_type',
              'entity.Shot.code', 'entity.CustomEntity02.code', 'entity', 'entity.Shot.sg_sequence', 'sg_latestversion']
    taskslist = find_shotgun('Task', filters, fields, sg_instance=sg_instance)
    task_dic = {}
    for task in taskslist:
        try:
            sequence = task['entity.Shot.sg_sequence']
            scene = sequence['name'] if sequence else None
            # pp.pprint(task)
            if not task['entity']:
                continue
            version_f = task['sg_latestversion'] or 0
            if version_f == 0 or version_f < 100:
                if project_name == 'DSF':
                    version_f = '100'
            dic_value = {'id': task['id'],
                         'scene': scene,
                         'shot': task['entity.Shot.code'][len(scene) + 1:] if (task['entity.Shot.code'] and scene) else None,
                         'code': task['entity.' + task['entity']['type'] + '.code'],
                         'type': task['entity']['type'],
                         'task_name': task['content'],
                         'step': task['step.Step.short_name'],
                         'step_code': task['step.Step.code'],
                         'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                         'classify': task['entity.Asset.sg_asset_type'],
                         'version': str(version_f).zfill(3), }
        except KeyError:
            print u'这个任务有问题：', task
            continue
        try:
            task_dic.update({task['entity.' + task['entity']['type'] + '.code'] + '_' + task['content']: dic_value})
        except TypeError:
            print u'这个任务有问题：', task
            continue
    return task_dic


def get_task(project_name, task_id, sg_instance=False):
    filters = [['project', 'name_is', project_name], ['id', 'is', task_id]]
    fields = ['content', 'step', 'step.Step.short_name', 'step.Step.code', 'entity.Asset.code', 'entity.Asset.sg_asset_type',
              'entity.Shot.code', 'entity.Episode.code', 'entity.CustomEntity02.code', 'entity',
              'entity.Shot.sg_sequence', 'sg_latestversion', 'task_reviewers']
    task = find_one_shotgun('Task', filters, fields, sg_instance=sg_instance)
    sequence = task['entity.Shot.sg_sequence']
    scene = sequence['name'] if sequence else None
    # pp.pprint(task)
    version_f = task['sg_latestversion'] or 0
    if version_f == 0 or int(version_f) < 100:
        if project_name == 'DSF':
            version_f = '100'
    dic_value = {'id': task['id'],
                 'project': project_name, 
                 'episodes': task['entity.Episode.code'] or '',
                 'scene': scene,
                 'shot': task['entity.Shot.code'][len(scene) + 1:] if (task['entity.Shot.code'] and scene) else None,
                 'code': task['entity.' + task['entity']['type'] + '.code'],
                 'type': task['entity']['type'],
                 'task_name': task['content'],
                 'step': task['step.Step.short_name'],
                 'step_code': task['step.Step.code'],
                 'classify': task['entity.Asset.sg_asset_type'],
                 'version': str(int(version_f) + 1).zfill(3),
                 "task_reviewers": task["task_reviewers"],
                 'date': datetime.datetime.now().strftime('%Y-%m-%d')}
    return dic_value


def get_version(project_name, version_id, sg_instance=False):
    filters = [['project', 'name_is', project_name], ['id', 'is', version_id]]
    fields = ["code", "description", "sg_status_list", "sg_version_number", 'sg_task.Task.sg_approve_version',
              "sg_path_to_frames", "sg_path_to_movie", "id", "user", 'path', 'sg_path_to_geometry',
              'sg_task.Task.sg_publish_version', 'entity', 'sg_task', 'entity.Asset.sg_asset_type',
              'entity.Shot.sg_sequence', 'sg_version_type', 'entity.Shot.code', 'sg_task.Task.step.Step.code']
    version = find_one_shotgun('Version', filters, fields, sg_instance=sg_instance)
    sequence = version['entity.Shot.sg_sequence']
    scene = sequence['name'] if sequence else None
    dic_value = {'id': version['id'], 'scene': scene, 'code': version['entity']['name'], 'version_code': version['code'],
                 'shot': version['entity.Shot.code'][len(scene) + 1:] if version['entity.Shot.code'] else None,
                 'sg_version_number': version['sg_version_number'], 'sg_path_to_frames': version['sg_path_to_frames'],
                 'step_code': version['sg_task.Task.step.Step.code'],
                 'sg_path_to_movie': version['sg_path_to_movie'], 'description': version['description'] or '',
                 'sg_path_to_geometry': version['sg_path_to_geometry'] or '', 'type': version['entity']['type'],
                 'task_name': version['sg_task']['name'], 'task_id': version['sg_task']['id'],
                 'classify': version['entity.Asset.sg_asset_type'], 'version': version['sg_version_number'],
                 'sg_version_type': version['sg_version_type'],
                 'sg_publish_version': version['sg_task.Task.sg_publish_version'],
                 'sg_approve_version': version['sg_task.Task.sg_approve_version'], }
    return dic_value


def get_no_version(project_name, code, sg_instance=False):
    filters = [['project', 'name_is', project_name], ['code', 'is', code], ['sg_version_number', 'is', None],
        ['sg_version_type', 'is', 'Submit']]
    fields = ["code", "description", "sg_status_list", "sg_version_number", "sg_path_to_frames", "sg_path_to_movie",
              "id", "user", 'path', 'sg_path_to_geometry', 'entity', 'sg_task', 'entity.Asset.sg_asset_type',
              'entity.Shot.sg_sequence', 'entity.Shot.code']
    version = find_one_shotgun('Version', filters, fields, sg_instance=sg_instance)
    if not version:
        return {}
    sequence = version['entity.Shot.sg_sequence']
    scene = sequence['name'] if sequence else None
    dic_value = {'id': version['id'], 'scene': scene, 'code': version['code'],
                 'shot': version['entity.Shot.code'][len(scene) + 1:] if version['entity.Shot.code'] else None,
                 'sg_version_number': version['sg_version_number'], 'sg_path_to_frames': version['sg_path_to_frames'],
                 'sg_path_to_movie': version['sg_path_to_movie'], 'sg_path_to_geometry': version['sg_path_to_geometry'],
                 'type': version['entity']['type'], 'task_name': version['sg_task']['name'],
                 'classify': version['entity.Asset.sg_asset_type'],
                 'version': str(version['sg_version_number']).zfill(3)}
    return dic_value


def get_latest_version(project_name, task_id, sg_instance=False):
    filters = [['project', 'name_is', project_name], ['id', 'is', task_id]]
    fields = ['sg_latestversion']
    taskdetail = find_shotgun('Task', filters, fields, sg_instance=sg_instance)
    if taskdetail:
        if taskdetail[0]['sg_latestversion']:
            return taskdetail[0]['sg_latestversion']
        else:
            if project_name == "DSF":
                return '100'
            return '000'
    else:
        return '000'


def update_shotgun(entity_type, entity_id, kwargs, sg_instance=False):
    return __sg_operate_doit('update', [entity_type, entity_id, kwargs], sg_instance=sg_instance)
    # try:
    #     return sg.update(entity_type, entity_id, kwargs)
    # except Exception as e:
    #     print u'更新出现错误: ', e
    #     return update_shotgun(entity_type, entity_id, kwargs)


def create_shotgun(entity_type, kwargs, sg_instance=False):
    return __sg_operate_doit('create', [entity_type, kwargs], sg_instance=sg_instance)
    # try:
    #     return sg.create(entity_type, kwargs)
    # except Exception as e:
    #     print u'创建出现错误: ', e
    #     return create_shotgun(entity_type, kwargs)


def upload_shotgun(entity_type, entity_id, path, field_name=None, display_name=None, sg_instance=False):
    return __sg_operate_doit('upload', [entity_type, entity_id, path, field_name, display_name], sg_instance=sg_instance)
    # try:
    #     return sg.upload(entity_type, entity_id, path, field_name, display_name)
    # except Exception, e:
    #     print '上传缩略图错误', e
    #     return None


def find_shotgun(entity_type, filters, fields, order=None, sg_instance=False):
    return __sg_operate_doit('find', [entity_type, filters, fields, order], sg_instance=sg_instance)
    # new_filters = filters
    # new_fields = fields
    # new_order = order
    # # new_filters = common_methods.change_dict_encoding(filters, encoding='gbk')
    # # new_fields = common_methods.change_dict_encoding(fields, encoding='gbk')
    # # new_order = common_methods.change_dict_encoding(order, encoding='gbk')
    # try:
    #     # print 'before data:', filters, '\n'
    #     find_result = sg.find(entity_type, new_filters, new_fields, new_order)
    #     return find_result
    # except Exception, e:
    #     print u'查询出现错误，', e
    #     return find_shotgun(entity_type, new_filters, new_fields, new_order)


def find_one_shotgun(entity_type, filters, fields, sg_instance=False):
    return __sg_operate_doit('find_one', [entity_type, filters, fields], sg_instance=sg_instance)
    # new_filters = filters
    # new_fields = fields
    # # new_filters = common_methods.change_dict_encoding(filters, encoding='gbk')
    # # new_fields = common_methods.change_dict_encoding(fields, encoding='gbk')
    # try:
    #     final_result = sg.find_one(entity_type, new_filters, new_fields)
    #     return final_result
    # except Exception, e:
    #     print u'查询出现错误，', e
    #     return find_one_shotgun(entity_type, new_filters, new_fields)


def schema_field_read(type_text, sg_instance=False):
    return __sg_operate_doit('schema_field_read', [type_text], sg_instance=sg_instance)
    # return sg.schema_field_read(type_text)


def batch_shotgun(batch_data, sg_instance=False):
    return __sg_operate_doit('batch', [batch_data], sg_instance=sg_instance)
    # return sg.batch(batch_data)


def follow_shotgun(user, entity, sg_instance=False):
    return __sg_operate_doit('follow', [user, entity], sg_instance=sg_instance)


def followers_shotgun(entity, sg_instance=False):
    return __sg_operate_doit('followers', [entity], sg_instance=sg_instance)


def valid_operators():
    valid_dic = {
        'addressing': ['is', 'is_not', 'contains', 'not_contains', 'in', 'type_is', 'type_is_not', 'name_contains',
                       'name_not_contains', 'name_starts_with', 'name_ends_with'],

        'checkbox': ['is', 'is_not'],

        'currency': ['is', 'is_not', 'less_than', 'greater_than', 'between', 'not_between', 'in', 'not_in'],

        'date': ['is', 'is_not', 'greater_than', 'less_than', 'in_last', 'not_in_last', 'in_next', 'not_in_next',
                 'in_calendar_day', 'in_calendar_week', 'in_calendar_month', 'in_calendar_year', 'between', 'in',
                 'not_in', ],

        'date_time': ['is', 'is_not', 'greater_than', 'less_than', 'in_last', 'not_in_last', 'in_next', 'not_in_next',
                      'in_calendar_day', 'in_calendar_week', 'in_calendar_month', 'in_calendar_year', 'between', 'in',
                      'not_in'],

        'duration': ['is', 'is_not', 'greater_than', 'less_than', 'between', 'in', 'not_in'],

        'entity': ['is', 'is_not', 'type_is', 'type_is_not', 'name_contains', 'name_not_contains', 'name_is', 'in',
                   'not_in', ],

        'float': ['is', 'is_not', 'greater_than', 'less_than', 'between', 'in', 'not_in'],

        'image': ['is', 'is_not'],

        'list': ['is', 'is_not', 'in', 'not_in'],

        'multi_entity': ['is', 'is_not', 'type_is', 'type_is_not', 'name_contains', 'name_not_contains', 'in',
                         'not_in'],

        'number': ['is', 'is_not', 'less_than', 'greater_than', 'between', 'not_between', 'in', 'not_in'],

        'password': [],

        'percent': ['is', 'is_not', 'greater_than', 'less_than', 'between', 'in', 'not_in'],

        'serializable': [],

        'status_list': ['is', 'is_not', 'in', 'not_in'],

        'summary': [],

        'tag_list': ['is', 'is_not', 'name_contains', 'name_not_contains', 'name_id'],

        'text': ['is', 'is_not', 'contains', 'not_contains', 'starts_with', 'ends_with', 'in', 'not_in'],

        'timecode': ['is', 'is_not', 'greater_than', 'less_than', 'between', 'in', 'not_in'],

        'url': []

    }
    return valid_dic


def get_filter_operators():
    filter_conditions = ['nane_is', 'name_contains', 'name_not_contains', 'name_starts_with', 'name_ends_with']
    return filter_conditions


def get_path_convention(project, _type, upload_type, sg_instance=False):
    filters = [['project', 'name_is', project], ['sg_type', 'is', _type], ['sg_upload_type', 'is', upload_type], ]
    fields = ['sg_work_file_name', 'sg_workfile_no_version', 'sg_prev_file_name', 'sg_prevfile_no_version',
        'sg_attachment_path', 'sg_attachment_no_version', 'sg_pattern', 'sg_oss_submit_path', 'description', 'sg_feedback_path']
    path_file_dic = find_one_shotgun('CustomEntity01', filters, fields, sg_instance=sg_instance)
    path_file_dic = {k: (v or '') for k, v in path_file_dic.items()}
    # print path_file_dic
    return path_file_dic


def download_attachment_shotgun(attachment, file_path=None, sg_instance=False):
    return __sg_operate_doit('download_attachment', [attachment, file_path], sg_instance=sg_instance)
    # return sg.download_attachment(attachment, file_path)


def type_menu():
    type_menu = ['Asset', 'Shot', 'Task', 'Sequence', 'Version', 'Note']
    return type_menu


def get_permission(login, sg_instance=False):
    if isinstance(login, int):
        permission = find_one_shotgun('Group', [['id', 'is', login]], ['sg_permission_group'], sg_instance=sg_instance)
    else:
        permission = find_one_shotgun('Group', [['sg_login', 'is', login]], ['sg_permission_group'], sg_instance=sg_instance)
    return permission['sg_permission_group']


def get_user_autumn_config(login, sg_instance=False):
    config = find_one_shotgun('Group', [['sg_login', 'is', login]], ['sg_autumn_config'], sg_instance=sg_instance)
    all_configs = []
    if not config:
        return None
    for cfg in config['sg_autumn_config']:
        config_content = find_one_shotgun(cfg['type'], [['id', 'is', cfg['id']]], ['sg_configs'], sg_instance=sg_instance)
        if config_content['sg_configs']:
            all_configs.append(config_content['sg_configs'])
    return all_configs


def get_autumn_config_codes(project_name, sg_instance=False):
    all_codes = find_shotgun('CustomEntity73', [['project', 'name_is', project_name]], ['code'], sg_instance=sg_instance)
    return [code['code'] for code in all_codes]


def set_autumn_config(config_code, config_content, sg_instance=False):
    config_entity = find_one_shotgun('CustomEntity73', [['code', 'is', config_code]], ['id'], sg_instance=sg_instance)
    return update_shotgun('CustomEntity73', config_entity['id'], {'sg_configs': config_content}, sg_instance=sg_instance)


def get_autumn_config(config_code, sg_instance=False):
    config_entity = find_one_shotgun('CustomEntity73', [['code', 'is', config_code]], ['sg_configs'], sg_instance=sg_instance)
    return config_entity['sg_configs']


def autumn_design_permissions():
    return ['admin']


def schema_field_read_shotgun(entity_type, field_name=None, project_entity=None, sg_instance=False):
    return __sg_operate_doit('schema_field_read', [entity_type, field_name, project_entity], sg_instance=sg_instance)
    # return sg.schema_field_read(entity_type, field_name, project_entity)


def note_thread_read_shotgun(note_id, entity_fields=None, sg_instance=False):
    return __sg_operate_doit('note_thread_read', [note_id, entity_fields], sg_instance=sg_instance)


if __name__ == '__main__':
    pprint.pprint(get_version('DSF', 25954))
