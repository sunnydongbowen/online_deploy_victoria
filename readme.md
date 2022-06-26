## 项目介绍

本项目是基于centos8，kolla-ansible容器化安装，部署openstack Victoria版本，总结出的一套自动化部署方法，简化了部署过程

## 运行环境

- 操作系统: CentOS Linux release 8.3.2011,桌面版
- openstack版本: Victoria
- 部署工具: kolla-ansible容器化安装

## 部署步骤

### 1、前提条件

- 服务器存储，为了确保环境稳定性，尽可能三块硬盘，满足ceph3副本需要

- 至少双网卡，且网卡名尽可能一致(服务器规格一致，网卡名一般是相同的)

- 为保证云平台流畅运行，内存性能尽可能满足在20G以上

### 2、设置域名解析和免密登录

[参考《多节点基于kolla-ansible的openstack安装部署》 1.5章节  ](https://github.com/sunnydongbowen/online_deploy_victoria/blob/master/%E5%A4%9A%E8%8A%82%E7%82%B9%E5%9F%BA%E4%BA%8Ekolla-ansible%E7%9A%84openstack%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20.md)

### 3、部署节点执行

> 在部署节点执行，尽量保证只执行一次，尽管脚本里做了很多判断，但重复执行依然可能会出现冲突，会把[多节点基于kolla-ansible的openstack安装部署](https://github.com/sunnydongbowen/online_deploy_victoria/blob/master/%E5%A4%9A%E8%8A%82%E7%82%B9%E5%9F%BA%E4%BA%8Ekolla-ansible%E7%9A%84openstack%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20.md)文档中的需要手动搭建的大部分都执行

```
python3 online_install_deploynode.py
```

### 4、非部署节点执行

> 在非部署节点执行

```
python3 online_install_notdeploynode.py
```

### 5、执行ceph安装脚本

> 所有节点执行，会[ceph搭建](https://github.com/sunnydongbowen/online_deploy_victoria/blob/master/ceph%E6%90%AD%E5%BB%BA.md)能手动执行的执行完成，执行前需要把cephadm文件上传到所有节点的/root目录下！

```
python online_ceph_install_allnode.py
```

### 6、修改登录密码

> 这一步key-passwd不需要执行了，已经写在脚本里，如果需要修改密码，可以在password.yml修改，不需要修改可以安装完成后查看密码即可。

[参考《多节点基于kolla-ansible的openstack安装部署》 1.8章节](https://github.com/sunnydongbowen/online_deploy_victoria/blob/master/%E5%A4%9A%E8%8A%82%E7%82%B9%E5%9F%BA%E4%BA%8Ekolla-ansible%E7%9A%84openstack%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20.md)

### 7、执行ceph安装

> 部署节点执行，[ceph搭建](https://github.com/sunnydongbowen/online_deploy_victoria/blob/master/ceph%E6%90%AD%E5%BB%BA.md) 从1.8 执行到1.16执行完！有报错的话要解决报错！

### 8、执行ceph脚本

> 部署节点执行，这个脚本主要是修改ceph.conf文件和替换，需要在上面执行成功后，再执行。
>

```
python online_ceph_cc_deploynode.py
```

### 9、拷贝文件到其他节点

> 把部署节点/etc/ceph目录下面这四个文件，scp到另外几个节点的/etc/ceph目录下。

![image-20210430102344348](image/image-20210430102344348.png)

### 10、修改multinode和globals.yml文件

  >  这两个文件很重要，要根据实际情况来改正确！multinode主要根据实际情况改主机名，节点分布情况，globals.yml主要改的是网卡，vip，以及嵌套环境的是qemu，物理环境是kvm等。

### 11、执行pull和deploy命令

部署节点执行[基于kolla-ansible的openstack安装部署](https://github.com/sunnydongbowen/online_deploy_victoria/blob/master/%E5%A4%9A%E8%8A%82%E7%82%B9%E5%9F%BA%E4%BA%8Ekolla-ansible%E7%9A%84openstack%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20.md)执行上面文档的1.14 -1.18即可，详细的见参考文档。中间会可能会遇到报错，根据实际情况解决。

### 12、解决热迁移失败问题

执行hot_migrate.py解决热迁移，失败问题

## 注意事项

- 本项目不涉及机密，全都基于开源openstack及开源软件
- 
- 提高速度，也可以进行半在线安装，把openstack的镜像和ceph的镜像打包好，openstack.zip. 先提前导入即可，这样不需要花很多时间在pull镜像这一步了

