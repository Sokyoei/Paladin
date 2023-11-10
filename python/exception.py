"""
Python Exception

https://docs.python.org/zh-cn/3/library/exceptions.html
https://docs.python.org/zh-cn/3/library/exceptions.html#exception-hierarchy
"""


class SokyoeiError(RuntimeError):
    """Sokyoei'Error sample"""


class AhriError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return super().__str__()


class NonoError(Exception):
    pass


try:
    raise SokyoeiError("Sokyoei Error")
except SokyoeiError as e:
    print(e)


exit(0)

########################################################################################################################
# Builtins exceptions error and warning
########################################################################################################################
BUILTINS_EXCEPTION_ERROR_WARNING = {
    BaseException: {
        BaseExceptionGroup: "",
        SystemExit: "sys.exit()",
        KeyboardInterrupt: "用户按键中断",
        GeneratorExit: "",
        Exception: {
            StopIteration: "迭代器迭代完成",
            StopAsyncIteration: "",
            ArithmeticError: {  # 算数类异常
                FloatingPointError: "",
                OverflowError: "算数结果过大",
                ZeroDivisionError: "对0做除法或取余时引发",
            },
            ExceptionGroup[BaseExceptionGroup]: "",
            AssertionError: "assert 断言失败",
            AttributeError: "属性引用或赋值失败",
            BufferError: "",
            EOFError: "input() 函数未读取到任何数据到达 EOF",
            ImportError: {ModuleNotFoundError: ""},
            LookupError: {KeyError: "dict 找不到指定的键", IndexError: "下标越界"},
            MemoryError: "内存不足",
            NameError: {UnboundLocalError: "变量未被赋值时被使用"},  # 某个局部或全局名称没有找到
            WindowsError: "OSError",
            IOError: "OSError",
            EnvironmentError: "OSError",
            OSError: {
                BlockingIOError: "",
                ChildProcessError: "",
                ConnectionError: {
                    BrokenPipeError: "",
                    ConnectionAbortedError: "",
                    ConnectionRefusedError: "",
                    ConnectionResetError: "",
                },
                FileExistsError: "",
                FileNotFoundError: "文件路径错误",
                InterruptedError: "",
                IsADirectoryError: "路径是一个文件夹",
                NotADirectoryError: "路径不是一个文件夹",
                PermissionError: "",
                ProcessLookupError: "给定进程不存在",
                TimeoutError: "",
            },
            ReferenceError: "",
            RuntimeError: {NotImplementedError: "", RecursionError: "超过解释器最大递归深度"},
            SyntaxError: {IndentationError: {TabError: ""}},  # 语法错误  # 缩进错误
            SystemError: "解释器内部错误",
            TypeError: "类型错误",
            ValueError: {UnicodeError: {UnicodeDecodeError: "", UnicodeEncodeError: "", UnicodeTranslateError: ""}},
            # Warning
            Warning: {
                BytesWarning: "",
                DeprecationWarning: "弃用警告",
                EncodingWarning: "",
                FutureWarning: "",
                ImportWarning: "",
                PendingDeprecationWarning: "",
                ResourceWarning: "",
                RuntimeWarning: "",
                SyntaxWarning: "",
                UnicodeWarning: "",
                UserWarning: "",
            },
        },
    }
}
