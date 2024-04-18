# Paladin([Python](https://www.python.org/))

1. 为避免整数频繁申请和销毁内存空间，Python 定义了一个小整数池`[-5, 256]`，这些整数对象是提前建立好的，不会被垃圾回收。
2. Python 解释器中使用了 `intern(字符串驻留)` 技术来提高字符串效率，如果有空格或长度超过 20 个字符，不启用 intern 机制。
3. Python 的 import 寻找路径为 `sys.path()`，环境变量是 `PYTHONPATH`。
4. Python 官方的包管理器是 [pip](pip.md)，第三方库发布网址是 [PyPI](https://pypi.org/) 。
5. [Conda](Conda.md) 是第三方包管理器。

## Python 源码打包、二进制构建

=== "setup.py"

    ```shell
    # 源码打包 tar.gz/zip
    python setup.py sdist

    # 二进制构建 egg/whl
    python setup.py bdist_egg
    python setup.py bdist_wheel

    # 安装
    python setup.py install
    # or
    pip install .

    # 安装（开发）
    python setup.py develop
    # or
    pip install -e .
    ```

=== "pyproject.toml"

    ```shell
    # 源码打包、二进制构建
    python -m build
    ```

## The Zen of Python, by Tim Peters 「Python 之禅」

=== "English"

    ```txt
    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    ```

=== "Chinese"

    ```txt
    优美优于丑陋
    明了优于隐晦
    简单优于复杂
    复杂优于凌乱
    扁平优于嵌套
    稀疏优于稠密
    可读性很重要
    即使实用比纯粹更优
    特例亦不可违背原则
    错误绝不能悄悄忽略
    除非它明确需要如此
    面对不确定性，拒绝妄加猜测
    任何问题应有一种，且最好只有一种，显而易见的解决方法
    尽管这方法一开始并非如此直观，除非你是那个荷兰人
    做优于不做
    然而不假思索还不如不做
    很难解释的，必然是坏方法
    很好解释的，可能是好方法
    命名空间是个绝妙的主意，我们应好好利用它！
    ```
