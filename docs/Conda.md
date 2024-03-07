# [Conda](https://docs.conda.io/en/latest/)

- [Anaconda](https://www.anaconda.com/)
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)

## 新建环境

```shell
conda create -n env_name python=python_version
```

## 删除环境

```shell
conda env remove -n env_name
# or
conda remove -n env_name --all
```

## 克隆环境

```shell
conda create -n env_name2 --clone env_name
```

## 导出配置

```shell
conda env export > environment.yml
```

## 从 environment.yml 创建环境

```shell
conda env create -f environment.yml
```

## 按照 environment.yml 升级环境

```shell
conda env update -n env_name --file environment.yml
```

## 打包环境

```shell
conda pack -n env_name
```

## 打包环境激活

```shell
cd ~/conda_dir/envs
# 解压环境
tar -zxvf env_name
conda activate env_name
```

## conda 更新

```shell
conda update conda
# `conda update conda` conda 未更新时执行
conda update -n base -c defaults conda --repodata-fn=repodata.json
```

## conda 离线安装

```shell
conda install --use-local package_name.tar.bz2
# or
conda install -c local package_name.tar.bz2
```

## 清理缓存

```shell
conda clean -a -y
```
