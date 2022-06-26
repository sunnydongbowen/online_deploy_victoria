'''
此脚本使用于：centos8.3_2011系统，
             v版本，
            在线安装
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

def images_load():
    images_list=['ceph-grafana.tar', 'ceph.tar', 'chrony.tar','cinder-api.tar', 'cinder-backup.tar', 'cinder-scheduler.tar', 'cinder-volume.tar', 'cron.tar', 'etcd.tar', 'fluentd.tar', 'glance-api.tar', 'haproxy.tar', 'heat-api-cfn.tar', 'heat-api.tar', 'heat-engine.tar', 'horizon.tar', 'keepalived.tar', 'keystone-fernet.tar', 'keystone-ssh.tar', 'keystone.tar', 'kolla-toolbox.tar', 'kuryr-libnetwork.tar', 'mariadb-clustercheck.tar', 'mariadb-server.tar', 'memcached.tar', 'neutron-dhcp-agent.tar', 'neutron-l3-agent.tar', 'neutron-metadata-agent.tar', 'neutron-openvswitch-agent.tar', 'neutron-server.tar', 'nova-api.tar', 'nova-compute.tar', 'nova-conductor.tar', 'nova-libvirt.tar', 'nova-novncproxy.tar', 'nova-scheduler.tar', 'nova-ssh.tar', 'openvswitch-db-server.tar', 'openvswitch-vswitchd.tar', 'placement-api.tar', 'rabbitmq.tar', 'registry.tar', 'zun-api.tar', 'zun-cni-daemon.tar', 'zun-compute.tar', 'zun-wsproxy.tar']
    for i in  images_list:
        command = 'cd /root/openstack  && docker load < '+ " "+ i
        logger.debug("导入离线"+i+"镜像")
        res = subprocess.getoutput(command)
        logger.debug(res)
        print()
    logger.debug("全部镜像导入完成")

images_load()