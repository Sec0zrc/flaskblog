2025.04.04更新

一个基于个人使用的简介的博客系统，前后端分离。
只是一个练手项目，目的是熟悉HTML、JavaScript、CSS基础。现在实现了博客的基本功能，包括用户注册、登录、登出、文章发布、编辑、删除、文章浏览，剩下的功能等之后有时间再实现。

## 技术栈
* HTML、CSS、JavaScript基础
* Python的flask库
* faker： 用于生成测试数据
* Flask-SQLAlchemy 
* Flask-jwt-extended 实现jwt认证登录
* redis：通过redis来实现用户账户登出
* Flask-restful：实现RESTful API资源
* Bootstrap 5：开源前端框架
* https://tabler.io/admin-template 基于bootstrap5开发的一个后端模板
* editor.md ：一款开源的Markdown编辑器
* marked.js：前端用于渲染Markdown的JavaScript库

## 功能
目前已实现功能：
1. 用户管理，支持用户注册、登录、登出
2. 博客管理，支持文章的发布、编辑、删除
3. 文章浏览
待实现功能：
* 评论管理，支持评论的回复、删除、审核
* 文章分类、标签页面
* 实时动态刷新JWT令牌

## 项目结构

```
├─blog
│  │  .env          # 环境变量，配置参数设置
│  │  commands.py   # 测试用例生成
│  │  config.py     # 配置文件
│  │  errors.py     # error处理
│  │  extension.py  # 扩展配置文件
│  │  models.py     # SQLAlchemy模型
│  │  run.py        
│  │  views.py      # 视图处理
│  │  __init__.py
│  │  
│  ├─api            # RESTful API资源实现
│  │  │  __init__.py
│  │  │  
│  │  ├─auth
│  │  │  └─  routes.py
│  │  ├─categories
│  │  │  └─  routes.py
│  │  ├─posts
│  │  │  └─  routes.py
│  │  ├─tags
│  │  │  └─  routes.py
│  │  ├─users
│  │  │  └─  routes.py
│  ├─static         # 静态资源
│  │  │  
│  │  ├─editormd
│  │  │  └─plugins
│  │  └─images
│  ├─templates      # flask模板文件
└─tests             # 单元测试
```


## 数据库设计

### 核心数据表
#### users用户表

| 字段名           | 类型           | 说明                 |
| ------------- | ------------ | ------------------ |
| user_id       | int(11)      | 主键，自增              |
| username      | varchar(50)  | 唯一，用于登录            |
| password_hash | varchar(255) | 密码加密存储             |
| create_at     | datetime     | 注册时间               |
| status        | tinyint(1)   | 登录状态（0表示未登录，1表示登录） |

索引：
* 唯一索引：`username`
* 普通索引：`create_at`
#### posts文章表
记录文章的信息

| 字段名         | 类型           | 说明                         |
| ----------- | ------------ | -------------------------- |
| post_id     | int(11)      | 主键，自增                      |
| user_id     | int(11)      | 外键->user.user_id           |
| title       | varchar(255) | 文章标题                       |
| content     | TEXT         | 文章内容                       |
| category_id | int(11)      | 外键->categories.categroy_id |
| status      | tinyint(1)   | 状态（0草稿，1发布，2私密）            |
| create_at   | datetime     | 发布时间                       |

索引：
* 外键索引：`user_id`，`categroy_id`
* 复合索引：`status`，`create_at`


#### categories 分类表

| 字段名         | 类型          | 说明       |
| ----------- | ----------- | -------- |
| categroy_id | int(11)     | 主键，自增    |
| name        | varchar(50) | 分类名称（唯一） |

索引:
唯一索引：`name`

#### tags 标签表

| 字段名         | 类型          | 说明       |
| ----------- | ----------- | -------- |
| tag_id      | int(11)     | 主键，自增    |
| name        | varchar(50) | 标签名称（唯一） |

索引：同分类表
#### comments评论表

| 字段名        | 类型          | 说明                                |
| ---------- | ----------- | --------------------------------- |
| comment_id | int(11)     | 主键，自增                             |
| post_id    | int(11)     | 外键->posts.post_id                 |
| user_id    | int(11)     | 外键->users.user_id(可以为空)           |
| parent_id  | int(11)     | 自关联，-->comments.comment_id(回复父评论) |
| content    | text        | 评论内容                              |
| status     | tinyint(1)  | 状态（0待审核，1通过，2不通过）                 |
| create_at  | datetime    | 评论时间                              |
| ip_address | varchar(45) | 记录评论者ip                           |
索引：
外键索引：post_id, user_id
普通索引：parent_id（处理层级回复）

#### post_tag_category 文章-标签分类关联表


| 字段名         | 类型      | 说明                         |
| ----------- | ------- | -------------------------- |
| post_id     | int(11) | 外键->posts.post_id          |
| categroy_id | int(11) | 外键->categroies.categroy_id |
| tag_id      | int(11) | 外键->tags_tag_id            |


