"""
Example of how to use setuptools
"""

from setuptools import setup, find_packages


# from submodule1 import __version__      # 1) 从 submodule1.__init__.__version__ 获得版本号
# __version__ == "0.0.1-dev"              # 2) 或直接在本地定义 version

setup(
    # 3) 或依据 tag 动态获得版本号(参考文档 <git release flow>)
    version_command='git describe --always',     # 如果采用 1) 或 2) 方式，则使用指令 `version=__version__`
    # `--always` 如果没有打过标签会出现错误信息 `fatal: No names found, cannot describe anything.`，这个参数将返回 commit hash number 代替 tag 以避免错误.

    name = "mymodules",
    packages = find_packages(exclude=['tests', '*.tests', '*.tests.*']),

    ########
    # 打包规则
    #
    # 定义 src 目录下的子包的打包规则
    package_data = {
        # 任何包中含有 .properties 文件，都包含它
        '':[ 'config/*.properties', '*.md' ],
        # 只包含 submodule1 的 data 文件夹中的 *.dat 和 *.dat1 文件
        'submodule2': ['data/*.dat', 'data/*.dat1'],
    },
    #include_package_data = True,
)
