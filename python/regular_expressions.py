"""
Regular Expressions 正则表达式
"""

import re

STR = "-215624168#1_0"

pattern_ = re.compile(r"(\d)", re.ASCII)
print(pattern_)

# 匹配一次
print(re.match(pattern_, "2Popstar Ahri2").groups())  # 从头开始匹配一个
print(re.fullmatch(r"(\d).*", "2Popstar Ahri2", re.ASCII).group())  # 整个字符串必须匹配
print(re.search(pattern_, "Popstar Ahri2").group())  # 任意位置匹配一个

# 匹配所有
print(re.findall(r"(\d*)#", "-215624168#1_0"))
piter = re.finditer(r"(\d)", "-215624168#1_0")
for p in piter:
    print(p.group())

# 匹配切分
print(re.split(r"(\d+)", "123w32r456", 2, re.ASCII))

# 匹配替换
print(re.sub(r"(\d)", "3", "Popstar Ahri2", 1, re.ASCII))
print(re.subn(r"(\d)", "3", "Popstar Ahri2", 1, re.ASCII))

# re.escape()
# re.error()

re.purge()  # clean cache
