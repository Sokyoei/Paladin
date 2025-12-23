# flask_learn

## 项目结构

```text
flask_learn
├──api          跟前端交互的接口
├──config       配置
├──crud         实现增删改查
├──enums        枚举
├──models       数据模型
├──schemas      数据校验
├──services     业务逻辑
├──static       静态资源
├──templates    模板
├──utils        实用工具
└──main.py      程序入口
```

## 运行项目

```shell
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Flask-Migrate 数据库迁移

```shell
# 初始化迁移环境
flask --app main.py db init
# 生成迁移文件
flask --app main.py db migrate
# 执行迁移
flask --app main.py db upgrade
```
