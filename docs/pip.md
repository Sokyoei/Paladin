# pip

## 导出配置

```powershell
pip freeze --all | Out-File requirements.txt -Encoding utf8
```

```shell
pip freeze --all > requirements.txt
```

## 从 requirements.txt 安装包

```shell
pip install -r requirements.txt
```
