# nginx

[nginx](https://nginx.org/en/) 是一个高性能的 HTTP 和反向代理 web 服务器

## 常用命令

nginx 默认的配置文件路径为 `/etc/nginx/nginx.conf`，配置文件的语法格式为 `ini` 文件。

```bash
# 测试 nginx.conf 文件语法是否正确
nginx -t
# 从文件中加载配置文件
nginx -c your_nginx.conf_path
# 重启 nginx
nginx -s reload -c your_nginx.conf_path
# 停止 nginx
nginx -s stop -c your_nginx.conf_path
```
