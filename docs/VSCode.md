# VSCode

## VSCode Container 离线环境配置

VSCode 离线环境需要固定 VSCode 版本，且需要对应的 `vscode-server` 版本。

```shell
# 下载 VSCode 离线安装包。
# Commit 可以在 VSCode 帮助 -> 关于中查看。
wget https://update.code.visualstudio.com/commit:$your_vscode_commit/server-linux-x64/stable

# 复制到容器内并解压。
# 宿主机
docker cp vscode-server-linux-x64.tar.gz $your_container_id_or_name:/root/
# 容器内
rm -rf /root/.vscode-server
mkdir -p /root/.vscode-server/bin/$your_vscode_commit
tar -zxf /root/vscode-server-linux-x64.tar.gz -C /root/.vscode-server/bin/$your_vscode_commit --strip-components=1
```
