# Pictor-Biological-Analysis-Platform

Pictor-Biological-Analysis-Platform（无码生信分析平台），生物大数据分析于一体平台,集成多个软件工具、标准化分析流程，并可自主定制分析流程，同时采用可视化、便捷化操作，大幅度提升数据分析效率。

# Todo

系统尚处于开发中第一阶段开发, 以下为目前的TODO

1. 完成待编写功能:

   1.1 工作区： 工作区筛选成员添加滚动条与搜索框 , 工作区动态区分工作区
      
   1.2 文件数据： 数据完成离线下载, 复制和移动功能， 进一步模块化 文件数据 功能, 使其独立成一个可配置模块， 上传功能修复 异步多文件 同时上传产生的问题
      
   1.3 完成上传规则设置
      
   1.4 添加站内信功能, 完善邮箱通知模板
      
3.整理代码/整理文档/整理设计图
   
4.编写分析任务管理接口, 对接平台

5.封装第一版本为Docker , 并发布 v1 Demo 

### 下一阶段

next next next next next next 

# 系统描述

致力于打造一个完整的无码生信分析平台，采用现阶段流行技术实现。

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

## 三. 功能说明

# 部署使用说明

## 自行部署


```shell script
git clone git@github.com:bioLacaille/Pictor.git  # clone

cd Pictor

python3 -m venv pictor_env
```



# 项目展示

# 版权声明

商业和自媒体转载前务必联系作者

个人转载请注明作者和仓库地址

# 许可证

[MIT](https://github.com/PanJiaChen/vue-element-admin/blob/master/LICENSE)

Copyright (c) 2020-present BioLacaille Team 
