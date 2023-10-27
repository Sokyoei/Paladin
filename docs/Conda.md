# [Conda](https://docs.conda.io/en/latest/)
- [Anaconda](https://www.anaconda.com/)
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)

## 新建环境

```shell
conda create -n env_name python=3.12
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

## 清理缓存

```shell
conda clean -a
```
