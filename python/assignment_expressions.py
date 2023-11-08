"""
Assignment Expressions   赋值表达式
walrus operator          海象运算符
var_name := exp or value
"""

import sys

a = 15
if a > 10:
    print("hello")

if sys.version_info >= (3, 8):
    if (a := 15) > 10:
        print("hello, walrus operator")

    n = 5
    while (n := n - 1) + 1:
        print("no")
