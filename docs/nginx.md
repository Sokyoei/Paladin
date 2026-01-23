# nginx

## 常用命令

nginx 默认的配置文件路径为 `/etc/nginx/nginx.conf`，配置文件的语法格式为 `ini` 文件。

```bash
# 测试 nginx.conf 文件语法是否正确
nginx -t
# 从文件中加载配置文件
nginx -c your_nginx.conf_path
```
