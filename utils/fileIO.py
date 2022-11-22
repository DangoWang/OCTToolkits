#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Wang donghao
# Date  : 2019.7
# wechat : 18250844478
###################################################################
import os
import shutil
import subprocess
from dayu_widgets.qt import *
from config import GLOBAL
import time
from utils import shotgun_operations
sg = shotgun_operations


def get_copy_list(source_dir, target_dir):
    #  把文件夹-->文件夹转为文件-->文件
    #  ('C:/a/', 'D:/b/') --> [['C:/a/a.txt', 'D:/b/cc.txt'], [], []...]
    if not source_dir:
        return []
    files = []
    for f in os.listdir(source_dir):
        source_file = source_dir + '/' + f
        target_file = target_dir + '/' + f
        if os.path.isfile(source_file):
            files.append([source_file, target_file])
        if os.path.isdir(source_file):
            files.extend(get_copy_list(source_file, target_file))
    return files


class LinkClient:

    def __init__(self):
        # self.client = client.OCT_RPC_CLIENT(host="sg.octmedia.com", port=9090)
        from thirdparty.oct_rpc import client
        self.client = client.OCT_RPC_CLIENT(host="sg.ds.com", port=9090)


class FormRPCCopy(QThread):
    finished = Signal(bool)
    progress = Signal(list)

    def __init__(self, mode, copy_list=[]):
        super(FormRPCCopy, self).__init__()
        # mode : upload, download
        self.mode = mode
        self.copy_list = copy_list
        self.__client = LinkClient

    def run(self, *args, **kwargs):
        i = 0.0
        __len = float(len(self.copy_list))
        try:
            if self.mode in ['download']:
                for copy_tuple in self.copy_list:
                    i += 1.0
                    self.__client.client.aliyun_download([copy_tuple])
                    self.progress.emit([os.path.split(copy_tuple[0])[-1], 100.0*i/__len])
            elif self.mode in ['upload']:
                for copy_tuple in self.copy_list:
                    i += 1.0
                    self.__client.client.aliyun_upload([copy_tuple])
                    self.progress.emit([os.path.split(copy_tuple[0])[-1], 100.0 * i / __len])
            self.finished.emit(True)
        except:
            self.finished.emit(False)


class CopyFile(QThread):
    finished = Signal(bool)
    progress = Signal(list)

    def __init__(self, copy_list=''):
        super(CopyFile, self).__init__()
        self.copy_list = copy_list
        self.copy_num = 0.0
        self.__copy_tuples = []
        # copy_list: [['C:/a/a.txt', 'D:/b/cc.txt'], [], []...]

    def run(self):
        copy_tuples = []
        if not self.copy_list:
            self.finished.emit(True)
            return
        #  先把所有的文件夹--文件夹变成文件--文件
        for ct in self.copy_list:
            if os.path.isdir(ct[0]):
                copy_tuples.extend(get_copy_list(ct[0], ct[1]))
            if os.path.isfile(ct[0]):
                copy_tuples.append([ct[0], ct[1]])
        self.__copy_tuples = [f for f in copy_tuples if '.db' not in f[0]]
        # thread_pool = ThreadPool(8)
        copied = []
        self.copy_num = 0.0
        # _args = []
        # all_copied = []
        for i, each in enumerate(self.__copy_tuples):
            if each[1] in copied:
                self.copy_num += 1.0
                continue
            copied.append(each[1])
            dest_path = os.path.dirname(each[1])
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
                # os.remove(each[1])
            # _args.append(each)
            self.concurrency_copy_file(each)
            # all_copied.append(thread_pool.apply_async(self.concurrency_copy_file, args=(each,)))
        # thread_pool.close()
        # thread_pool.join()
        # if all_copied:
        self.finished.emit(True)

    def concurrency_copy_file(self, each):
        # if os.path.isfile(each[0]):  # 如果是文件的话
        try:
            if os.path.isfile(each[1]):
                a = time.localtime(os.stat(each[0]).st_mtime)
                b = time.localtime(os.stat(each[1]).st_mtime)
                mTimeS = time.strftime('%Y-%m-%d %H:%M:%S', a)
                mTimeD = time.strftime('%Y-%m-%d %H:%M:%S', b)
                s_size = os.path.getsize(each[0])
                d_size = os.path.getsize(each[1])
                if mTimeS == mTimeD and s_size == d_size:  # 如果修改日期和大小完全一致，不拷贝
                    pass
                else:
                    shutil.copy2(each[0], each[1])
            else:
                shutil.copy2(each[0], each[1])
            self.copy_num += 1.0
            # print self.copy_num*100.0/float(len(self.copy_list))
            self.progress.emit([each[0].split('/')[-1].split('\\')[-1],
                                self.copy_num*100.0/float(len(self.__copy_tuples))])
            return each[0]
        except Exception as e:
            print u'CopyFile ERROR', e
            # self.finished.emit([])
            return False


class CopyFTP(QThread):
    finished = Signal(bool)
    progress = Signal(list)

    def __init__(self, copy_list=''):
        super(CopyFTP, self).__init__()
        self.copy_list = copy_list
        self.source = ''
        self.exe = GLOBAL.CURRENTSCRIPTPATH + '\\bin\\ossutil64\\ossutil64.exe'
        # endpoint = "http://oss-cn-qingdao.aliyuncs.com"
        # AccessKeyID = "LTAI4FrNYVGzL3HQCVvCdpQ8"
        # AccessKeySecret = "M0AKHtV0cD2ctVo9Z6k9p0cWYBXqmN"
        # path = 'oss://oss-oct-sg/'
        self.__endpoint = "https://oss-cn-qingdao.aliyuncs.com"
        self.__AccessKeyID = "LTAI4FrNYVGzL3HQCVvCdpQ8"
        self.__AccessKeySecret = "M0AKHtV0cD2ctVo9Z6k9p0cWYBXqmN"

    def run(self):
        if not self.copy_list:
            return
        copied = []
        for i, each in enumerate(self.copy_list):
            # if not os.path.isfile(each[0]) and not os.path.isdir(each[0]):
            #     print u'请检查该路径是否正确： ', each[0]
            #     continue
            if each[0] in copied:
                continue
            copied.append(each[0])
            try:
                cmd = u'{exe} -e {endpoint} -i {AccessKeyID} -k {AccessKeySecret} cp -r "{path}" "{cppath}" --update'.format(
                    **{
                        'exe': self.exe,
                        'endpoint': self.__endpoint,
                        'AccessKeyID': self.__AccessKeyID,
                        'AccessKeySecret': self.__AccessKeySecret,
                        'path': u'{0}'.format(each[0]),
                        'cppath': u'{0}'.format(each[1] if not each[0].startswith('oss:') else each[1].rstrip(each[1].split('/')[-1].split('\\')[-1]))
                    })
                print cmd
                returned_value = subprocess.check_call(cmd.encode('gbk'), stdout=subprocess.PIPE)  # returns the exit code
            except Exception as e:
                print u'上传阿里云错误', e
                return
            self.progress.emit([each[0].split('/')[-1].split('\\')[-1], float(i+1)*100.0 / float(len(self.copy_list))])
        self.finished.emit(True)


class DownloadUrlFile(QThread):
    """
    拷贝文件线程
    """
    finished = Signal(bool)  # 拷贝完成信号
    progress = Signal(dict)  # 正在拷贝的文件名和进度

    def __init__(self, attachments_dict=''):
        super(DownloadUrlFile, self).__init__()
        self.attachments_dict = attachments_dict
        #  attachments_dict:{下载路径： 附件id列表}

    def run(self):
        folder_path = ''
        attachments_id = ''
        for key, value in self.attachments_dict.items():
            folder_path = key
            attachments_id = value
        attachment_list = sg.find_shotgun("Attachment", [["id", "in", attachments_id]], ["this_file"])
        i = 0.0
        for file_url in attachment_list:
            i += 1.0
            attachment = file_url["this_file"]
            local_file_path = folder_path + "/" + file_url["this_file"]["name"]
            sg.download_attachment_shotgun(attachment, file_path=local_file_path)
            progress = int(i * 100 / float(len(attachment_list)))
            self.progress.emit(progress)
        self.finished.emit(True)


class FormRPCDownloadUrlFile(QThread):
    """
    拷贝文件线程
    """
    finished = Signal(bool)  # 拷贝完成信号
    progress = Signal(dict)  # 正在拷贝的文件名和进度

    def __init__(self, attachments_dict=''):
        super(FormRPCDownloadUrlFile, self).__init__()
        self.attachments_dict = attachments_dict
        self._copy_from_oss = CopyFTP()
        self._copy_from_oss.progress.connect(self.progress.emit)
        self._copy_from_oss.finished.connect(self.finished.emit)
        #  attachments_dict:{下载路径： 附件id列表}

    def run(self):
        copy_path_list = []
        folder_path, attachments_id = self.attachments_dict.items()[0]
        attachment_list = sg.find_shotgun("Attachment", [["id", "in", attachments_id]], ["this_file"])
        i = 0.0
        for file_url in attachment_list:
            i += 1.0
            attachment = file_url["this_file"]
            command = LinkClient()
            try:
                oss_path = command.client.sg_download_attachment(attachment)
            # oss路径 = func(file_url["this_file"]) #  这里通知rpc去从shotgun下载临时文件到oss
                file_name = os.path.split(oss_path)[-1]
                copy_path_list.append([oss_path, u'{0}/{1}'.format(folder_path, file_name)])  # 调用
                progress = int(i * 100 / float(len(attachment_list)))
                self.progress.emit(progress)
            except Exception as e:
                print u"呼叫下载超时", e
        self._copy_from_oss.copy_list = copy_path_list
        self._copy_from_oss.start()


if __name__ == '__main__':
    pass
    # print os.path.isdir('I:/dsf/Asset/CH/NH_XiZ/RIG/sourceimages/2048/.mayaSwatches')
    # print os.path.getsize(r'D:\problem_fixing\tex\maya\dsf_BaB_tex.ma')
    # print os.path.getsize(r'D:\problem_fixing\tex\maya\dsf_BaB_tex_2.ma')
    # import time
    # start = time.clock()
    # aaa = shutil.copyfile(r'D:\problem_fixing\tex\maya\dsf_BaB_tex.ma', r'D:\problem_fixing\tex\maya\dsf_BaB_tex2.ma')
    # print aaa
    # elapsed = (time.clock() - start)
    # print elapsed
    #
    # start = time.clock()
    # def f1vsf2(name1, name2):
    #     f1 = open(name1)
    #     f2 = open(name2)
    #     line1 = f1.readline()
    #     line2 = f2.readline()
    #     diff = False
    #     while line1:
    #         if line1 != line2:
    #             diff = True
    #             break
    #         line1 = f1.readline()
    #         line2 = f2.readline()
    #     f1.close()
    #     f2.close()
    #     return diff
    # print f1vsf2(r'D:\problem_fixing\tex\maya\dsf_BaB_tex.ma', r'D:\problem_fixing\tex\maya\dsf_BaB_tex2.ma')
    # elapsed = (time.clock() - start)
    # print elapsed
