# coding: utf-8
#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Mon Dec  9 13:47:47 2019
#========================================
import json, pickle
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from rpc_schema import OCT_RPC
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class OCT_RPC_CLIENT(object):
    '''
    '''
    def __init__(self, host, port, timeout=60):
        transport = TSocket.TSocket(host, port)
        transport.setTimeout(timeout*1000)

        self.transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        self.client = OCT_RPC.Client(protocol)
        self.transport.open()



    def __del__(self):
        '''
        '''
        self.transport.close()




    def hello(self):
        '''
        test connection
        '''
        result = self.client.hello()
        return result




    def aliyun_upload(self, file_list_data):
        '''
        dst: Local  path
        src: Aliyun path
        '''
        result = self.client.aliyun_upload(json.dumps(file_list_data))
        return result





    def aliyun_download(self, file_list_data):
        '''
        src: Aliyun path
        dst: Local  path
        '''
        result = self.client.aliyun_download(json.dumps(file_list_data))
        return result





    def call_sg(self, mode, data):
        '''
        '''
        result = self.client.call_sg(mode, pickle.dumps(data))
        return pickle.loads(result)




    def sg_download_attachment(self, sg_file_info):
        '''
        '''
        result = self.client.sg_download_attachment(pickle.dumps(sg_file_info))
        return result
