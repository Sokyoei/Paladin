# FastAPI

## 项目结构

```text
fastapi_learn
├──api          跟前端交互的接口
├──config       配置
├──crud         实现增删改查
├──models       数据模型
├──schemas      数据校验
├──services     业务逻辑
├──sql          SQL 语句
├──utils        实用工具
└──main.py      程序入口
```

## 运行项目

```bash
cd fastapi_learn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# python main.py
```

## 数据库迁移

```bash
cd fastapi_learn
alembic list_templates                      # 查看模板
alembic init alembic -t async               # 初始化 alembic

alembic revision --autogenerate -m "init"   # 生成迁移文件

alembic upgrade head                        # 升级数据库
```
