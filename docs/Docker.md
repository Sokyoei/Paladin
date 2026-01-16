# Docker

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
            "https://docker.xuanyuan.me/"
        ]
    }
    ```

2. 重启 Docker 服务

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```
