# Docker

[Docker](https://www.docker.com/)

## 离线安装

下载离线二进制文件和文件压缩包

```bash
# docker
wget https://download.docker.com/linux/static/stable/x86_64/docker-27.5.1.tgz
# docker compose
wget https://github.com/docker/compose/releases/download/v5.6.0/docker-compose-linux-x86_64
# docker buildx
wget https://github.com/docker/buildx/releases/download/v0.38.0/buildx-v0.38.0.linux-amd64
```

上传到离线机上

```bash
# docker
tar -zxvf docker-27.5.1.tgz
sudo cp docker/* /usr/local/bin/

# docker compose/docker buildx
sudo mkdir -p /usr/local/lib/docker/cli-plugins/
sudo cp docker-compose-linux-x86_64 /usr/local/lib/docker/cli-plugins/docker-compose
sudo cp buildx-v0.38.0.linux-amd64 /usr/local/lib/docker/cli-plugins/docker-buildx
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx
# 验证是否安装成功
docker compose version
docker buildx version
```

创建 `service` 文件

```bash
sudo tee /etc/systemd/system/containerd.service > /dev/null << 'EOF'
[Unit]
Description=containerd container runtime
Documentation=https://containerd.io
After=network.target local-fs.target

[Service]
#uncomment to enable the experimental sbservice (sandboxed) version of containerd/cri integration
#Environment="ENABLE_CRI_SANDBOXES=sandboxed"
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/local/bin/containerd
Type=notify
Delegate=yes
KillMode=process
Restart=always
RestartSec=5
LimitNPROC=infinity
LimitCORE=infinity
LimitNOFILE=infinity
TasksMax=infinity
OOMScoreAdjust=-999

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/docker.service > /dev/null << 'EOF'
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target docker.socket firewalld.service containerd.service time-set.target
Wants=network-online.target containerd.service
Requires=docker.socket

[Service]
Type=notify
ExecStart=/usr/local/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutStartSec=0
RestartSec=2
Restart=always
StartLimitBurst=3
StartLimitInterval=60s
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
Delegate=yes
KillMode=process
OOMScoreAdjust=-500

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/docker.socket > /dev/null << 'EOF'
[Unit]
Description=Docker Socket for the API

[Socket]
# If /var/run is not implemented as a symlink to /run, you may need to
# specify ListenStream=/var/run/docker.sock instead.
ListenStream=/run/docker.sock
SocketMode=0660
SocketUser=root
SocketGroup=docker

[Install]
WantedBy=sockets.target

EOF
```

添加用户组

```bash
sudo groupadd docker

# 添加当前用户到 docker 组，可以直接 docker xxx 而不是必须 sudo docker xxx
sudo usermod -aG docker $USER
```

启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now containerd
sudo systemctl enable --now docker.socket
sudo systemctl enable --now docker.service

# 验证
sudo systemctl status containerd
sudo systemctl status docker.socket
sudo systemctl status docker
```

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
# 查看所有容器
docker ps -a
# 运行镜像
docker run -p
# 运行容器
docker start container_id__or__container_name
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
