"""
如果目录中存在 __init__.py 文件，那么 Python 视其为模块。
"""

__version__="0.0.2"


def init():
    from submodule1.funcs import hello2
    from submodule1.funcs.hello2 import greeting
    # print("hello world twice!! - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    hello2.greeting()
