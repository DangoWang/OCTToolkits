# coding: utf-8
#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Mon Dec  9 13:40:00 2019
#========================================
import os

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol 
from thrift.server import TServer

import logging
from logging.handlers import TimedRotatingFileHandler

from rpc_schema import OCT_RPC
import rpc_env
from server_class import aliyun, shotgun
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
logger = logging.getLogger('oct_rpc')
logger.setLevel(level=logging.INFO)

fomater = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
handle = TimedRotatingFileHandler(rpc_env.LOG_FILE_PATH,
                                  when='D',
                                  backupCount=rpc_env.LOG_FILE_COUNT,
                                  encoding='utf-8')

handle.setLevel(logging.INFO)
handle.setFormatter(fomater)
logger.addHandler(handle)


class OCT_RPC_SERVER(shotgun.Shotgun, aliyun.Aliyun):
    '''
    '''
    def __init__(self):
        '''
        '''
        super(OCT_RPC_SERVER, self).__init__()



    def hello(self):
        '''
        '''
        return 'hello my frirend...'




    def sg_download_attachment(self, sg_file_info):
        '''
        '''
        local_file_path  = self.download_attachment(sg_file_info, rpc_env.LOCAL_TMP_PATH)
        local_dir_path   = os.path.dirname(local_file_path)
        aliyun_path = u'{0}/{1}'.format(rpc_env.OSS_TMP_PATH, os.path.basename(local_dir_path))
        if self.aliyun_transfer(local_dir_path, aliyun_path):
            return u'{0}/{1}'.format(aliyun_path, os.path.basename(local_file_path))
        else:
            return str()




def main():
    '''
    '''
    processor = OCT_RPC.Processor(OCT_RPC_SERVER())
    transport = TSocket.TServerSocket('0.0.0.0', port=rpc_env.PORT)

    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    logger.info('RPC-Server start success...')
    server = TServer.TForkingServer(processor, transport, tfactory, pfactory)
    server.serve()




if __name__ == '__main__':
    main()
