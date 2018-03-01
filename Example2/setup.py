"""
Example of how to use setuptools
"""

# 命令行："python setup.py --version" 可以获得版本号。
from submodule2 import __version__                    # 1) 从 submodule1.__init__.__version__ 获得版本号
# __version__ = "0.0.2"                               # 2) 或直接在本地定义 version

# 安装 dependenices. 因为 bug 的原因, 需要将 url 分开处理，分别传给 `install_requires` 和 `dependency_links`
def install_deps():
    new_pkgs = []
    links = []
    with open('requirements.txt') as f:
        default = f.readlines()
        for resource in default:
            if 'git+http' in resource:
                links.append(resource.strip())
                #pkg = resource.split('#')[-1]
                #new_pkgs.append(pkg.replace('egg=', '').rstrip())
            else:
                new_pkgs.append(resource.strip())
    return new_pkgs, links

new_pkgs, links = install_deps()

# 可以让 submodule2 在安装前检查依赖的版本，并自动升级到最新版(依赖必须发布到 pipy 中，否则会因为无法找到而出错)：
# autoupgrade 0.2.0 之后才支持 master, 需要手工安装：pip install https://bitbucket.org/jorkar/autoupgrade/get/master.tar.gz --trusted-host=bitbucket.org
# 或python -m pip install git+https://bitbucket.org/jorkar/autoupgrade.git@master#autoupgrade-0.2.0 --trusted-host=bitbucket.org
#from autoupgrade import AutoUpgrade
#AutoUpgrade("submodule1", index="https://pypi.company.com/repos").upgrade_if_needed()

from setuptools import setup, find_packages
# 打包前执行 `git tag -a $(python setup.py --version)`　将 __version__ 注册为 tag number
setup(
    author='Jeff Wang',
    author_email='jeffwji@test.com',

    version_command='git describe --always --long --dirty=-dev',  # 3) 获得　tag 动态获得版本号(参考文档 <git release flow>)
    # `--always` 如果没有打过标签会出现错误信息 `fatal: No names found, cannot describe anything.`，这个参数将返回 commit hash number 代替 tag 以避免错误.
    # `--long --dirty=-dev` 获得长格式版本信息： <version>-<times>-<commit-hash>-<dirty> 例如：0.0.2-0-g00bd0b4-dev

    name = "submodule2",
    packages = find_packages(
        exclude=['tests', '*.tests', '*.tests.*']
    ),

    ########
    # 打包规则
    #
    # 定义 src 目录下的子包的打包规则，缺省 setup.py 只打包 py 文件，如果希望加入其他文件，需要在 package_data 中定义。
    package_data = {
        # 任何包中含有 .properties 文件，都包含它
        '':[ 'config/*.properties', '*.md', 'requirements.txt' ],
        # 只包含 submodule1 的 data 文件夹中的 *.dat 和 *.dat1 文件
        'submodule2': ['data/*.dat', 'data/*.dat1'],
    },
    # MANIFEST.in 文件用于定义其他不存在于 `package_data`(包含 __init__.py ) 范围内的文件。
    install_requires=new_pkgs,
    dependency_links=links,
)
