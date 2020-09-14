# Pictor-Biological-Analysis-Platform

Pictor-Biological-Analysis-Platform（无码生信分析平台）

# Todo

系统尚处于开发中第一阶段开发, 以下为目前的TODO

1. 完成待编写功能:

   1.1 工作区： 工作区筛选成员添加滚动条与搜索框 , 工作区动态区分工作区
      
   1.2 文件数据： 数据完成离线下载, 复制和移动功能， 进一步模块化 文件数据 功能, 使其独立成一个可配置模块， 上传功能修复 异步多文件 同时上传产生的问题
      
   1.3 完成上传规则设置
      
   1.4 添加站内信功能, 完善邮箱通知模板
      
3.整理代码/整理文档/整理设计图
   
4.编写分析任务管理接口, 对接平台

5.封装第一版本Docker , 并发布 v1 Demo 

# 系统描述

致力于打造一个完整的无码生信分析平台，采用 Python+Django+Vue+Element 实现

## 一. 用户角色描述

系统用户分为 用户, 超级用户, 管理员, 超级管理员四个等级

用户:  可使用项目/样本/数据/分析任务

超级用户:  可使用项目/样本/数据/分析任务/设置/统计图表

管理员: 可使用项目/样本/数据/分析任务/设置/统计图表/实时监控/管理

超级管理员: 目前与管理员一致, 为冗余角色, 用于后续增加系统运维功能后, 该角色可使用运维功能对系统进行维护

其中使用系统必须创建工作区, 工作区成员等级决定了当前用户对于项目/样本/数据/分析任务/设置的可操作功能, 管理员不受工作区工作区等级限制, 可操作任意功能

工作区成员等级：

游客: 可使用功能模块内的数据, 仅查看

普通成员: 可使用功能模块内的数据, 查看/编辑以及除了删除以外的操作

超级成员: 可使用功能模块内的数据, 在普通成员的基础上, 可进行删除操作

工作区管理员： 可使用功能模块内的数据, 任意操作

## 二. 项目架构

![技术架构](https://sagene-i-cloud-dev.s3.cn-north-1.amazonaws.com.cn/data/public/%E6%8A%80%E6%9C%AF%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1+.jpg)


## 三. 功能说明

![功能概述](https://sagene-i-cloud-dev.s3.cn-north-1.amazonaws.com.cn/data/public/Pictor%E5%8A%9F%E8%83%BD%E6%A6%82%E8%BF%B0.jpg)

## 四. 使用说明

# 部署使用说明

## 一. 自行部署

部署前提：
 
1.安装MySQL , 创建MySQL数据库 'pictor'

```shell script
create database pictor character set utf8;
```

2.安装Redis, nodejs(npm)


3.部署

```shell script
git clone git@github.com:bioLacaille/Pictor.git  # clone
```

配置 pictor_backend/configure.ini 里的 MYSQL 

```shell script
[MYSQL]
MYSQL_DB = pictor
MYSQL_USER = pictor
MYSQL_PASSWORD = pictor123456
MYSQL_HOST = 127.0.0.1
MYSQL_PORT = 3306

```

```shell script
# 部署并运行后端
python3 -m venv pictor_env
source pictor_env/bin/activate
cd pictor_backend
pip install -r requirements.txt
python manage.py makemigrations pictor
python manage.py migrate
python manage.py create_default_user  # 创建默认用户
python manage.py runserver 0.0.0.0:8000
```

```shell script
# 部署并运行前端
cd pictor_frontend
npm install
npm run serve
```

3.访问: http://127.0.0.1:8080

## 二. 自行封装docker

```shell script
docker build -t pictor .
```

```shell script
docker run -d -p 80:80  pictor sh -c 'sh init.sh'
```

等待初始化完毕(大概需要10s), 访问: http://127.0.0.1/

指定文件数据存放目录, 将目录挂载至 /deploy_web/PictorData 即可 

```shell script
docker run -d -p 80:80 -v {FILEDATA}:/deploy_web/PictorData pictor sh -c 'sh init.sh'
```

使用宿主MySQL数据库

```shell script
docker run -d -p 80:80 -v {MYSQLDATA}:/var/lib/mysql pictor sh -c 'sh init.sh'
```


## 三. 使用 docker demo 

亦可直接使用docker demo

```shell script
docker pull fualan/pictor_demo:latest
```

```shell script
docker run -d -p 80:80  fualan/pictor_demo sh -c 'sh init.sh'
```

等待初始化完毕(大概需要10s), 访问: http://127.0.0.1/


指定文件数据存放目录, 将目录挂载至 /deploy_web/PictorData 即可 

```shell script
docker run -d -p 80:80 -v {FILEDATA}:/deploy_web/PictorData fualan/pictor_demo sh -c 'sh init.sh'
```

使用宿主MySQL数据库

```shell script
docker run -d -p 80:80 -v {MYSQLDATA}:/var/lib/mysql fualan/pictor_demo sh -c 'sh init.sh'
```

ps: docker 版本为当前稳定版, 如需使用最新版, 请自行拉取代码进行部署

# 项目展示

## 首页

![首页](https://sagene-i-cloud-dev.s3.cn-north-1.amazonaws.com.cn/data/public/%E9%A6%96%E9%A1%B5.png)

## 数据管理

![数据管理](https://sagene-i-cloud-dev.s3.cn-north-1.amazonaws.com.cn/data/public/%E6%96%87%E4%BB%B6%E6%95%B0%E6%8D%AE.png)

## 分析任务

![](https://sagene-i-cloud-dev.s3.cn-north-1.amazonaws.com.cn/data/public/%E5%88%86%E6%9E%90%E4%BB%BB%E5%8A%A1.png)

## 任务详情

![](https://sagene-i-cloud-dev.s3.cn-north-1.amazonaws.com.cn/data/public/%E4%BB%BB%E5%8A%A1%E8%AF%A6%E6%83%85.png)

# 版权声明

商业和自媒体转载前务必联系作者

个人转载请注明作者和仓库地址

# 许可证

[MIT]

Copyright (c) 2020-present BioLacaille Team 
