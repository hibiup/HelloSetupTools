from unittest import TestCase


class TestJoke(TestCase):
    def test_hello_from_this(self):
        ''' 单元测试会自动发现同一项目中的模块，不会导致 import 失败。'''
        import submodule2
        submodule2.init()   # submodule2.__init__.init()

    def test_submodule1(self):
        ''' 先安装 submodule1，否则失败于找不到模块 '''
        import submodule1
        submodule1.init()   # submodule1.__init__.init()
