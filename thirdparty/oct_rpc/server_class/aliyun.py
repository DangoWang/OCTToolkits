#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Dec 10 17:29:08 2019
#========================================
import re
import json
import subprocess
import logging
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
logger = logging.getLogger('oct_rpc.Aliyun')


def convert_win_path(path):
    '''
    '''
    drive = re.match('[a-zA-Z]:', path)
    if not drive:
        return path

    linux_path = re.sub('^[a-zA-Z]:', '/data/{0}'.format(drive.group()[0].lower()), path).replace('\\', '/')
    return linux_path




class Aliyun(object):
    '''
    '''
    def __init__(self):
        '''
        '''
        pass





    def aliyun_upload(self, file_list_data):
        '''
        '''
        file_list = json.loads(file_list_data)
        result = list()
        for l in file_list:
            l[0] = convert_win_path(l[0])
            result.append(self.aliyun_transfer(l[0], l[1]))

        return all(result)





    def aliyun_download(self, file_list_data):
        '''
        '''
        file_list = json.loads(file_list_data)
        result = list()
        for l in file_list:
            l[1] = convert_win_path(l[1])        
            result.append(self.aliyun_transfer(l[0], l[1]))

        return all(result)





    def aliyun_transfer(self, src, dst):
        '''
        '''
        commands = u'ossutil64 cp -r {0} {1} --update'.format(src, dst)

        try:
            subprocess.check_call(commands, shell=True)
            logger.info('Trans file form {0} to {1} Success.'.format(src, dst))
            return True

        except:
            logger.error('Trans file form {0} to {1} Faild.'.format(src, dst), exc_info=True)
            return False
