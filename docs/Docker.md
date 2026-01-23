# Docker

## 常用命令

```bash
# 启动容器
docker run -d --name your_container_name/your_image_name
# 停止容器
docker stop your_container_name/your_image_name
# 构建容器，tag 可选，默认 lastest
docker build -t your_image_name[:tag] . -f your_Dockerfile_path
# 保存镜像
docker save -o image_name.tar image_name:latest
# 从 tar 中加载镜像
docker load -i image_name.tar
```

docker compose 命令

```bash
# 检查 docker-compose.yml 文件是否正确
docker compose config
# 启动服务（后台）
docker compose up -d
# 停止服务
docker compose down
# 重启服务
docker compose restart
# 构建镜像
docker compose build
# 启动服务并进入容器
docker compose run your_service_name
```

## FAQ

### Docker 配置不需要 root 权限

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
# 重启
```

### Docker 配置镜像加速

1. 配置文件 `/etc/docker/daemon.json`

    ```json
    {
        "registry-mirrors": [
            "https://docker.1ms.run/",
            "https://docker.xuanyuan.me/"
        ]
    }
    ```

2. 重启 Docker 服务

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```
