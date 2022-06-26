'''
此脚本使用于：centos8.3_2011系统，
             v版本，
            在线安装，非部署节点
'''
import subprocess
import logging
import time
import os
import socket
# 配置日志信息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    filename='install.log',
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

def about_firewall():
    '''
    关闭防火墙，可以重复跑
    '''
    logger.debug("开始关闭并禁用防火墙")
    command_stop = 'systemctl stop  firewalld && systemctl disable  firewalld'
    res_stop = subprocess.getoutput(command_stop)
    logger.debug(res_stop)
    if res_stop:
        logger.debug('关闭防火墙成功')
    print()

def mkdir():
    '''
    创建需要的目录，可以重复跑
    '''
    cinbin = '/opt/cni/bin'
    etckolla = '/etc/kolla'
    config_nova = '/etc/kolla/config/nova'
    config_glance = '/etc/kolla/config/glance'
    config_gnocchi = '/etc/kolla/config/gnocchi'
    config_backup = '/etc/kolla/config/cinder/cinder-backup'
    config_volume = '/etc/kolla/config/cinder/cinder-volume'

    def mdkir_sub(path_mkdir):
        if os.path.exists(path_mkdir):
            logger.debug(path_mkdir + "目录已经存在，不再创建")
        else:
            command_mkdir = 'mkdir -p' + ' ' + path_mkdir
            res_mkdir = subprocess.getoutput(command_mkdir)
            logger.debug(res_mkdir)

    mdkir_sub(cinbin)
    #mdkir_sub(etckolla)
    mdkir_sub(config_nova)
    mdkir_sub(config_glance)
    mdkir_sub(config_gnocchi)
    mdkir_sub(config_backup)
    mdkir_sub(config_volume)
    print()

def selinux():
    '''
    关闭selinux权限，可以重复跑
    '''
    logger.debug("开始关闭并禁用selinux")
    command = 'setenforce 0 ' + ' ' + '&&' + ' '+"sed -i '/^SELINUX=/c SELINUX=disabled' /etc/selinux/config"
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def timedate():
    '''
    调整时区，可以重复跑
    '''
    logger.debug("开始调整时区")
    command = 'timedatectl set-timezone Asia/Shanghai'
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def wget_aliyun():
    '''
    拉取阿里云docker-ce.repo,在线安装才需要执行，可以重复跑
    '''
    if os.path.exists('/etc/yum.repos.d/docker-ce.repo'):
        logger.debug('/etc/yum.repos.d/docker-ce.repo 文件已存在，不再下载')
    else:
        command = 'wget -P /etc/yum.repos.d/  https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo'
        logger.debug("开始安装docker阿里云")
        res = subprocess.getoutput(command)
        logger.debug(res)
        print()

def docker_online():
    '''
    在线安装才需要执行,可以重复跑
    '''

    command = 'rpm -e runc --nodeps'
    logger.debug("卸载runc")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'rpm -e --nodeps podman'
    logger.debug("卸载podman")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'yum -y install docker-ce-20.10.3-3.el8.x86_64 docker-ce-cli-20.10.3-3.el8.x86_64  containerd.io-1.4.3-3.1.el8'
    logger.debug("开始安装docker")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def changepip():
    '''
    可以重复跑
    '''
    if os.path.exists('/root/.pip'):
        logger.debug("/root/.pip 目录已存在，不在创建")
    else:
        command = 'mkdir ~/.pip'
        logger.debug("创建pip文件")
        res = subprocess.getoutput(command)
        logger.debug(res)
        print()

        command = 'touch /root/.pip/pip.conf && chmod 777 /root/.pip/pip.conf'
        logger.debug("创建pip.conf文件")
        res = subprocess.getoutput(command)
        logger.debug(res)
        print()

        f = open('/root/.pip/pip.conf', 'a', encoding='utf-8')
        f.write('[global]\n')
        f.write('index-url = https://mirrors.aliyun.com/pypi/simple/\n')
        f.write('[install]\n')
        f.write('trusted-host=mirrors.aliyun.com\n')
        f.close()

def updatepip():
    '''
    可以重复跑，尽量别重复
    '''
    command = 'pip3 install --upgrade pip'
    logger.debug("升级pip")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def install_rust():
    '''
    可以重复跑，尽量别重复
    '''
    command = 'pip3 install setuptools_rust'
    logger.debug("setuptools_rust")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def install_git():
    command = 'yum -y install git'
    logger.debug("安装git")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def ansible_online():
    command = 'pip3 install ansible==2.9.5'
    logger.debug("开始安装ansible")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def ansible_kolla_online():
    command = 'pip3 install PyYAML --ignore-installed PyYAML'
    logger.debug("解决PyYAML冲突问题")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'pip3 install kolla-ansible'
    logger.debug("安装kolla-ansible")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def copy_file():
        command = 'cp -r /usr/local/share/kolla-ansible/etc_examples/kolla/*  /etc/kolla/'
        logger.debug("拷贝kolla文件")
        res = subprocess.getoutput(command)
        logger.debug(res)
        print()

        command = 'cp /usr/local/share/kolla-ansible/ansible/inventory/* /etc/kolla/'
        logger.debug("拷贝文件")
        res = subprocess.getoutput(command)
        logger.debug(res)
        print()

def docker_aliyun():
    '''
    更换docker国内源
    '''
    if os.path.exists('/etc/docker'):
        logger.debug('/etc/docker目录已存在，不再创建')
    else:
        command = 'mkdir -p /etc/docker'
        logger.debug("创建文件")
        res = subprocess.getoutput(command)
        logger.debug(res)
        print()

    command = 'touch /etc/docker/daemon.json && chmod 777 /etc/docker/daemon.json'
    logger.debug("创建daemon.json文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    f = open('/etc/docker/daemon.json', 'a', encoding='utf-8')
    f.write('{\n')
    f.write('    "log-opts": {\n')
    f.write('        "max-file": "5",\n')
    f.write('        "max-size": "50m"\n')
    f.write('    },\n')
    # https://f9dk003m.mirror.aliyuncs.com
    # https://f9dk003m.mirror.aliyuncs.com
    f.write('    "registry-mirrors": ["https://f9dk003m.mirror.aliyuncs.com"]\n')
    f.write('}\n')
    f.close()

    command = 'systemctl daemon-reload'
    logger.debug("重新加载docker文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'systemctl enable docker && systemctl restart docker'
    logger.debug("重启docker")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def changeyml():
    count = 0
    yamlPath='/usr/local/share/kolla-ansible/ansible/roles/baremetal/vars/main.yml'
    with open('/usr/local/share/kolla-ansible/ansible/roles/baremetal/vars/main.yml', encoding='utf-8') as f, open('/usr/local/share/kolla-ansible/ansible/roles/baremetal/vars/main.bak', 'w', encoding='utf-8') as f1:
        for line in f:
            if count==5:
                # https://f9dk003m.mirror.aliyuncs.com
                # https://hub-mirror.c.163.com/
                line = '  registry-mirrors: ["https://f9dk003m.mirror.aliyuncs.com"]\n'
            # 写文件
            f1.write(line)
            count = count+1
    # 删除文件和重命名文件
    os.remove('/usr/local/share/kolla-ansible/ansible/roles/baremetal/vars/main.yml')
    os.rename('/usr/local/share/kolla-ansible/ansible/roles/baremetal/vars/main.bak', '/usr/local/share/kolla-ansible/ansible/roles/baremetal/vars/main.yml')

    command = 'chmod 777 /usr/local/share/kolla-ansible/ansible/roles/baremetal/vars/main.yml'
    logger.debug("修改yml文件权限")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def delete_libvirtsock():

    command = 'rm -rf /var/run/libvirt/libvirt-sock'
    logger.debug("删除文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'rm -rf /run/libvirt/libvirt-sock'
    logger.debug("删除/run下的libvirt-sock文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()


def pip_docker():
    command = 'pip3 install docker'
    logger.debug("安装docker模块")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def install_opentackclient():
    command = 'pip3 install python-openstackclient --ignore-installed PyYAML'
    logger.debug("安装openstackclient")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('10.0.0.1',8080))
        ip= s.getsockname()[0]
    finally:
        s.close()
    return ip

def dockerservice():
    # 读ip,这个根据实际情况，如果是单控制节点，其实读的不是本机ip，而是写第一个控制节点的ip就可以了，与etcd有关
    file1 = '/usr/lib/systemd/system/docker.service'
    file2 = '/usr/lib/systemd/system/docker.bak'
    # command = 'hostname -i'
    logger.debug("读取本机ip")
    # res = subprocess.getoutput(command)
    # logger.debug(res)
    res = get_host_ip()
    # 修改文件
    execstart= "/usr/bin/dockerd  -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock --cluster-store etcd://"+res+':2379'
    with open(file1,encoding='utf-8') as  f1,open(file2,'w',encoding='utf-8') as f2:
        for line in f1:
            if '/usr/bin/dockerd' in line:
                line = 'ExecStart='+execstart
                #line = line.replace('/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock',execstart)
                f2.write(line+'\n')
            else:
                f2.write(line)
        os.remove(file1)
        os.rename(file2,file1)

def restart_docker():
    command = 'systemctl daemon-reload'
    logger.debug("重新加载文件")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

    command = 'systemctl enable docker && systemctl restart docker'
    logger.debug("enable并重启docker")
    res = subprocess.getoutput(command)
    logger.debug(res)
    print()

if __name__ == '__main__':
    about_firewall()     # 关闭防火墙
    mkdir()              # 创建需要的目录
    selinux()            # 关闭selinux权限
    timedate()           # 修改时区
    wget_aliyun()        # 下载阿里云docker.repo
    docker_online()      # 在线安装docker
    changepip()          # 修改pip源为国内
    updatepip()          # 更新pip包
    install_git()        # 安装git
    install_rust()       # 安装setuptoolsrust
    #ansible_online()     # 在线安装ansible 2.9.5
    #ansible_kolla_online() # 在线安装kolla-ansible
    #copy_file()          # 复制kolla multinode，allinone，yml等文件
    docker_aliyun()      #  docker更换阿里云镜像
    #changeyml()          #  dockeryml修改
    delete_libvirtsock()  # 删除var/run/libvirt/libvirt-sock 文件
    dockerservice()  # 修改service文件
    restart_docker()  # 重启docker
    pip_docker()          # 安装docker模块
    install_opentackclient()   # 安装openstack客户端
    pass

