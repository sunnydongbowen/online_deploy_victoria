'''
此脚本使用于：centos8.3_2011系统，
             v版本，
            安装完成,最后执行，解决热迁移失败问题
'''
import subprocess
import logging
import time
import os
import  yaml
import socket
# 配置日志信息
logging.basicConfig(level= logging.DEBUG,
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

global text
text = r'''#!/usr/bin/perl
#
# This is a wrapper for dmidecode that will return the configured UUID
# when 'dmidecode -s system-uuid' is called. Otherwise, it will call dmidecode
# and return as appropriate.
#

use strict;
use warnings;
use IO::Handle;

# Desired System UUID
my $uuid;
my $exit=0;
my $sub=0;

# Read command line.
my $cla="";
foreach my $arg (@ARGV) { $cla.=$arg." "; }
$cla=~s/\s+$//;

if ($cla eq "-q -t 0,1,4,17")
{
        $sub=1;
}

# Read the UUID from /etc/libvirt/libvirtd.conf.
my $sc="</etc/libvirt/libvirtd.conf";
my $fh=IO::Handle->new();
open ($fh, $sc) or die "$!";
while (<$fh>)
{
        chomp;
        my $line=$_;
        next if $line =~ /^#/;
        if ($line =~ /host_uuid/)
        {
                ($uuid)=($line =~ /"(.*?)"/);
        }
}
$fh->close();

# Call the real dmidecode
$sc="/usr/sbin/dmidecode.orig $cla 2>&1 |";
$fh=IO::Handle->new();
open ($fh, $sc) or die $!;
while (<$fh>)
{
        chomp;
        my $line=$_;
        # If I found a UUID, this line is the UUID and I am doing a
        # substitution, well, do it already.
        if (($uuid) && ($line=~/(\s+)UUID: /) && ($sub))
        {
                my $space=$1;
                print "${space}UUID: $uuid\n";
        }
        else
        {
                print $line, "\n";
        }
}
$fh->close();
$exit=$?;

exit($exit);
'''

def mv():
    logger.debug("备份dmicode文件")
    command= 'mv /usr/sbin/dmidecode /usr/sbin/dmidecode.orig'
    res = subprocess.getoutput(command)
    logger.debug(res)
    if res:
        logger.debug('备份dmicode文件')
    print()

def writedm():
    logger.debug("重新写入dmidecode文件")
    f = open('/usr/sbin/dmidecode', 'a', encoding='utf-8')
    f.write(text)
    f.close()

def change():
    logger.debug("修改dmicode文件权限")
    command= 'chmod +x /usr/sbin/dmidecode'
    res = subprocess.getoutput(command)
    logger.debug(res)
    if res:
        logger.debug('修改dmicode文件')
    print()

def generate_uuid():
    logger.debug("生成uuid并写入文件")
    command= 'uuidgen'
    uuid = subprocess.getoutput(command)
    logger.debug(uuid)
    str_tmp = 'host_uuid = '+ '"'+uuid+'"'
    with open('/etc/kolla/nova-libvirt/libvirtd.conf','a',encoding='utf-8') as f:
        f.write(str_tmp+'\n')

def restart_container():
    logger.debug("重启相关容器")
    command= 'docker restart nova_compute nova_libvirt'
    res = subprocess.getoutput(command)
    logger.debug(res)

if __name__ == '__main__':
    mv()
    writedm()
    change()
    generate_uuid()
    restart_container()