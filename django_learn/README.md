# django_learn

## 项目结构

```text
django_learn
├──app
│  ├──migrations/   数据迁移目录
│  ├──admin.py      后台管理配置
│  ├──apps.py       应用配置
│  ├──models.py     数据模型定义
│  ├──tests.py      测试
│  └──views.py      视图定义
├──django_learn     项目配置目录
│  ├──asgi.py       ASGI 异步支持
│  ├──settings.py   项目配置
│  ├──urls.py       URL 和函数的对应关系
│  └──wsgi.py       WSGI 传统同步
└──manage.py        项目管理
```

## 创建项目和应用

```shell
django-admin startproject django_learn
cd django_learn
python manage.py startapp app
```

## 创建数据库

```shell
python manage.py makemigrations     # 创建迁移文件
python manage.py migrate            # 执行迁移
python manage.py createsuperuser    # 创建超级用户
```

## 运行项目

```shell
python manage.py runserver
```
