"""
Example of how to use setuptools
"""

import subprocess
from submodule1 import __version__                    # 1) 从 submodule1.__init__.__version__ 获得版本号
#__version__ = "0.0.2"                               # 2) 或直接在本地定义 version

from setuptools import setup, find_packages

# Read description from README file.
def long_description():
    from os import path
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()
    
def get_depends():
    with open('requirements.txt') as f:
        return f.read().splitlines()
    
# 命令行："python setup.py --version" 可以获得版本号。
def get_version():
    #return subprocess.check_output(['git', 'describe', '--always', '--tags', '--long', '--dirty=.dev']).decode('ascii').strip()
    return __version__

# 打包前执行 `git tag -a $(python setup.py --version)`　将 __version__ 注册为 tag number
setup(
    ########
    # Meta data
    #
    author='Jeff Wang',
    author_email='jeffwji@test.com',
    name="setuptoolsdemo",
    long_description=long_description(),
    
    ########
    # Versioning
    #
    version=get_version(),
    # version_command='git describe --always --tags --long --dirty=.dev',  # 3) 获得　tag 动态获得版本号(参考文档 <git release flow>)
    # `--always` 如果没有打过标签会出现错误信息 `fatal: No names found, cannot describe anything.`，这个参数将返回 commit hash number 代替 tag 以避免错误.
    # `--tags --long --dirty=-dev` 获得长格式版本信息： <tag>-<times>-<commit-hash>.<dirty> 例如：0.0.2-0-g00bd0b4.dev
    # 定制 version 的格式（必须先打 tag）
    #
    #version_format='{tag}.dev{commitcount}+{gitsha}',
    # setup_requires=['setuptools-git-version'],
    ########
    ## 数据文件打包规则
    #
    ### 指定或排除目录或模块：
    # find_package 想限制查找的访问，以下表示查找除了 tests 和 test 目录之外的所有其他目录下的项目文件。
    packages=find_packages(
        exclude=['tests', 'test']
    ),
    # 也可以直接指定只打包某些目录
    #   packages=['submodule1', 'submodule2']
    # 但是不会包含 module1/submoduleA 和 module/submoduleB。如果要包含其下子目录，需要改成:
    #   packages=find_packages()，或明确罗列每一个 submodule 的路径。
    #
    ### 打包格式：
    # 1）wheel 格式（推荐格式，需要安装 `pip install twine`）：
    # 打包命令：`python setup.py egg_info -bDEV bdist_wheel rotate -m.egg -k3`
    # 打包文件名：{dist}-{version}(-{build})?-{python_version}-{abi}-{platform}.whl
    #
    # 或 egg 格式（easy_install 格式）
    # 打包命令：`python setup.py egg_info -bDEV bdist_egg rotate -m.egg -k3`
    #
    # `egg_info` 参数打印出打包信息。
    # wheel 只打包 py 文件，如果希望加入其他文件，需要以下配置：
    #
    # `package_data` 用于将`子模块/子目录`（注意必须是`子模块/子目录`，既不能用于项目根，也不能用于`子目录`，或`子目录/子目录`下的文件）下的非代码文件。
    #package_data={
    #    # 模块（含有 __init__.py 文件）下的 conf 子目录下的任何包中含有 .properties 的文件。
    #    'mymodule': ['conf/*.properties'],
    #},
    #include_package_data=True,
    #
    # `data_files`（推荐）可以包含任意路径，包括根目录下的额外数据文件。
    data_files=[
        # 参数格式: (打包文件中的目录名称 , [源代码中的路径])。
        ('conf', ['conf/config.properties']),
    ],
    # wheel 格式中这些文件将被打包到 `[package]/<package_name-version>.data/data/` 路径下，比如将 `conf/conf.properties` 打包到
    # `[package]/<package_name-version>.data/data/conf/config.properties`。路径中的 `conf` 由 tuple 中第一个元素指定。
    #
    # egg 文件中文件被直接打包到包根目录的 `/conf/config.properties`，目录中的 `conf` 由 tuple 中的第一个元素指定。
    #
    # pip install 将数据（非模块）文件安装到 `$PYTHONPATH/conf/config.properties` 目录下。路径中的 `conf` 由 tuple 的第一个元素指定。
    #
    # pip 可以安装 wheel 格式但是不能安装 egg 文件。egg 通过 `python -m easy_install dist/xxx.egg` 来安装。
    #
    # 2）tar.gz 格式
    # 打包命令：`python setup.py egg_info -bDEV sdist rotate -m.egg -k3`
    #
    # `MANIFEST.in` 用于配置需要被打包的文件，可以指定任意文件，比如 项目根目录下的文件 README.md 等。
    #
    # MANIFEST.in 不工作于 wheel 等格式。它只对 sdist 打包参数生效。数据（非模块）文件安装到 `.venv/conf/conf.properties` 目录下。
    #
    
    ########
    #
    install_requires=get_depends(),
    
    ########
    #
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
