import subprocess
import logging
import time
import os
# 配置日志信息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    filename='cceph.log',
                    filemode='a')
# 定义一个Handler打印Debug及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# 设置日志打印格式
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger('install')
def cephconf():
    with open('/etc/ceph/ceph.conf',encoding='utf-8') as f1,open('/etc/ceph/ceph.bak','w',encoding='utf-8') as f2:
        for line in f1:
            line = line.lstrip()
            f2.write(line)
        os.remove('/etc/ceph/ceph.conf')
        os.rename('/etc/ceph/ceph.bak','/etc/ceph/ceph.conf')

def change():
    command = 'chmod -R 777  /etc/ceph'
    logger.debug("修改权限")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def copyfile():
    command = 'cp /etc/ceph/*  /etc/kolla/config/nova'
    logger.debug("复制文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'cp /etc/ceph/*   /etc/kolla/config/glance'
    logger.debug("复制文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'cp /etc/ceph/*  /etc/kolla/config/cinder/cinder-backup'
    logger.debug("复制文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'cp /etc/ceph/*  /etc/kolla/config/cinder/cinder-volume'
    logger.debug("复制文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'cp /etc/ceph/*  /etc/kolla/config/gnocchi'
    logger.debug("复制文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def  command():
    '''
    解决ceph warn问题
    '''
    command = 'ceph config set mon auth_expose_insecure_global_id_reclaim false'
    logger.debug("修改属性auth_expose_insecure_global_id_reclaim为false")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'ceph config set mon auth_allow_insecure_global_id_reclaim false'
    logger.debug("修改auth_allow_insecure_global_id_reclaim为false")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

if __name__ == '__main__':
   cephconf()
   change()
   copyfile()
   #command()
