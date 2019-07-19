from unittest import TestCase

'''
注意，因为这个项目包含多个 Example，每个 Example 都是一个独立的根项目，所以运行其中的测试案例的时候需要将执行目录切换到相应的案例根目录下，
否则会报告模块找不到。

存在 `<module_name>/tests` 目录下的单元测试会自动发现项目，不会导致 import 失效。
'''

from submodule1.funcs import hello2  # from 不能到文件级，文件只能 import
from submodule1 import hello


class TestJoke(TestCase):
    def test_hello(self):
        hello.greeting()
        hello2.greeting()

