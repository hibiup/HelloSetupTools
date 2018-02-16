"""
Example of how to use setuptools
"""

from setuptools import setup, find_packages

# 命令行："python setup.py --version" 可以获得版本号。

from submodule1 import __version__                    # 1) 从 submodule1.__init__.__version__ 获得版本号
# __version__ = "0.0.2"                               # 2) 或直接在本地定义 version

# 打包前执行 `git tag -a $(python setup.py --version)`　将 __version__ 注册为 tag number
setup(
    version_command='git describe --always --long --dirty=-dev',  # 3) 获得　tag 动态获得版本号(参考文档 <git release flow>)
    # `--always` 如果没有打过标签会出现错误信息 `fatal: No names found, cannot describe anything.`，这个参数将返回 commit hash number 代替 tag 以避免错误.
    # `--long --dirty=-dev` 获得长格式版本信息： <version>-<times>-<commit-hash>-<dirty> 例如：0.0.2-0-g00bd0b4-dev

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
