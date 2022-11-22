# coding: utf-8
#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Dec 10 17:22:26 2019
#========================================
import os
import shotgun_api3
from operator import methodcaller
import pickle
import logging
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
logger = logging.getLogger('oct_rpc.Shotgun')

class Shotgun(object):
    '''
    '''
    def __init__(self):
        '''
        '''
        self._sg = shotgun_api3.Shotgun('http://sg.ds.com', login='td-sg', ensure_ascii=False, password='octmedia-2019')




    def call_sg(self, mode, _data):
        '''
        '''
        new_data = pickle.loads(_data)
        try:
            result = methodcaller(mode, *new_data)(self._sg)
            return pickle.dumps(result or None)

        except:
            logger.error('Error to get shotgun data..', exc_info=True)
            return pickle.dumps(None)




    def download_attachment(self, sg_file_info, attachment_tmp_dir):
        '''
        '''
        _file_info = pickle.loads(sg_file_info)
        local_path = os.path.join(attachment_tmp_dir, str(_file_info['id']), _file_info['name'])
        if not os.path.isdir(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))

        result = self._sg.download_attachment(_file_info, local_path)
        return result
