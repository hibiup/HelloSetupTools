from unittest import TestCase

'''
存在 `<module_name>/tests` 目录下的单元测试会自动发现项目，不会导致 import 失效。
'''

import submodule2

class TestJoke(TestCase):
    def test_hello(self):
        submodule2.hello
