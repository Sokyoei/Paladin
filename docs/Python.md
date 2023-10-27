# [Python](https://www.python.org/) ([CPython](https://github.com/python/cpython))

1. 为避免整数频繁申请和销毁内存空间，Python 定义了一个小整数池`[-5, 256]`，这些整数对象是提前建立好的，不会被垃圾回收。
2. Python 解释器中使用了 `intern(字符串驻留)` 技术来提高字符串效率，如果有空格或长度超过 20 个字符，不启用 intern 机制。
3. Python 的 import 寻找路径为 `sys.path()`，环境变量是 `PYTHONPATH`。
4. Python 官方的包管理器是 `pip`，第三方库发布网址是 [PyPI](https://pypi.org/) 。
5. [Conda](Conda.md) 是第三方包管理器。

# The Zen of Python, by Tim Peters *「Python 之禅」*

> Beautiful is better than ugly. *「优美优于丑陋」*<br>
> Explicit is better than implicit. *「明了优于隐晦」*<br>
> Simple is better than complex. *「简单优于复杂」*<br>
> Complex is better than complicated. *「复杂优于凌乱」*<br>
> Flat is better than nested. *「扁平优于嵌套」*<br>
> Sparse is better than dense. *「稀疏优于稠密」*<br>
> Readability counts. *「可读性很重要*<br>
> Special cases aren't special enough to break the rules. *「即使实用比纯粹更优」*<br>
> Although practicality beats purity. *「特例亦不可违背原则」*<br>
> Errors should never pass silently. *「错误绝不能悄悄忽略」*<br>
> Unless explicitly silenced. *「除非它明确需要如此」*<br>
> In the face of ambiguity, refuse the temptation to guess. *「面对不确定性，拒绝妄加猜测」*<br>
> There should be one-- and preferably only one --obvious way to do it. *「任何问题应有一种，且最好只有一种，显而易见的解决方法」*<br>
> Although that way may not be obvious at first unless you're Dutch. *「尽管这方法一开始并非如此直观，除非你是荷兰人」*<br>
> Now is better than never. *「做优于不做」*<br>
> Although never is often better than *right* now. *「然而不假思索还不如不做」*<br>
> If the implementation is hard to explain, it's a bad idea. *「很难解释的，必然是坏方法」*<br>
> If the implementation is easy to explain, it may be a good idea. *「很好解释的，可能是好方法」*<br>
> Namespaces are one honking great idea -- let's do more of those! *「命名空间是个绝妙的主意，我们应好好利用它」*<br>
