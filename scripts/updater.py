# -*- coding: utf-8 -*-
from thirdparty import pika
import getpass
import os


def cmd_str():
    def get_symbolic_link():
        user = getpass.getuser()
        link_pass_tmp = 'C:/Users/' + user + '/Desktop/Oct Launcher2.0.lnk'
        link_pass = link_pass_tmp if os.path.isfile(link_pass_tmp) else link_pass_tmp.replace(user, 'Administrator')
        return link_pass
    symbolic_link = get_symbolic_link()
    if symbolic_link and os.path.isfile(symbolic_link):
        os.remove(symbolic_link)
    print 'starting updating...'
    src = '//oct.ds.com/TD/Tools/OCT_Toolkits/*'
    dst = '/cygdrive/d/Tools/OCT_Toolkits/'
    dest = r'D:\Tools\OCT_Toolkits'
    if not os.path.isdir(dest):
        os.makedirs(dest)
    cmds = []
    cmd1 = r'\\oct.ds.com\TD\Tools\install\rsync\3.1.2\bin\rsync.exe -av --exclude=*/.git/* --exclude=*/.idea/* {0} {1}'.format(
        src, dst)
    cmd2 = r'\\oct.ds.com\TD\Tools\install\rsync\3.1.2\bin\rsync.exe -av {0} {1}'.format(
        '//oct.ds.com/TD/Tools/OCT_Toolkits/OctLauncher2.1.lnk', r'/cygdrive/c/Users/%username%/Desktop/OctLauncher2.1.lnk')
    cmd3 = r'\\oct.ds.com\TD\Tools\install\rsync\3.1.2\bin\rsync.exe -av {0} {1}'.format(
        '//oct.ds.com/TD/Tools/OCT_Toolkits/OctLauncher2.1.lnk',
        r'/cygdrive/c/Users/%username%/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/OctLauncher2.1.lnk')
    cmds.append(cmd1)
    cmds.append(cmd2)
    cmds.append(cmd3)
    return cmds


def send_update_info(info):
    credential = pika.PlainCredentials('admin', '123456')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='mq.ds.com', virtual_host='/shotgun', credentials=credential))
    channel = connection.channel()
    # channel.exchange_declare(exchange='update', exchange_type='fanout', durable=True)
    channel.basic_publish(exchange='update', routing_key='', body=info)
    connection.close()


if __name__ == '__main__':
    all_cmds = cmd_str()
    for each in all_cmds:
        send_update_info(each)
