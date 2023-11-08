"""
Python 3.10: match ... case ...
"""

import sys

if sys.version_info >= (3, 10):
    flag = False
    match (100, 200):
        case (100, 300):
            print("Case 1")
        case (100, 200) if flag:
            print("Case 2")
        case (100, y):
            print(f"Case 3, y: {y}")
        case _:
            print("Case 4, I match anything!")
