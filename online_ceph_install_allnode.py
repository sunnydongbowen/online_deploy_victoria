import subprocess
import logging
import time
import os
# 配置日志信息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    filename='ceph.log',
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

def cephadm():
    # 拷贝文件到/usr/bin目录
    command = 'cd ~ ' + ' '+ '&&'+" cp cephadm /usr/bin"
    logger.debug("拷贝cephadm文件到/usr/bin目录")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'chmod +x /usr/bin/cephadm'
    logger.debug("修改cephadm文件权限")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def aliyun_epel():
    command = 'yum install -y https://mirrors.aliyun.com/epel/epel-release-latest-8.noarch.rpm'
    logger.debug("安装epel源")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = "sed -i 's|^#baseurl=https://download.example/pub|baseurl=https://mirrors.aliyun.com|' /etc/yum.repos.d/epel*"
    logger.debug("替换epel源为阿里云地址")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = "sed -i 's|^metalink|#metalink|' /etc/yum.repos.d/epel* "
    logger.debug("替换metalink")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def install_cephadm():
    command = "cephadm add-repo --release octopus "
    logger.debug("添加源")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = "cephadm install "
    logger.debug("安装cephadmin")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def install_ceph_comm():

    # 删除源
    command = "rm -rf /etc/yum.repos.d/ceph.repo"
    logger.debug("删除ceph.repo")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    # 复制源
    command = "cp /root/online_deploy_victoria/ceph.repo    /etc/yum.repos.d/"
    logger.debug("复制ceph.repo")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    # 安装ceph-common
    command = "cephadm install ceph-common "
    logger.debug("安装ceph-comm")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def mkdirceph():
    command = "mkdir -p /etc/ceph "
    logger.debug("创建/etc/ceph目录")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

if __name__ == '__main__':
    cephadm()
    aliyun_epel()
    install_cephadm()
    install_ceph_comm()
    mkdirceph()
