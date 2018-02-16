"""
Example of how to use setuptools
"""

from setuptools import setup, find_packages

# __version__ == 0.0.1

from submodule1 import __version__

setup(
    name = "mymodules",
    version = __version__,
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
