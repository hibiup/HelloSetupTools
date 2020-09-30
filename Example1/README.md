https://blog.ionelmc.ro/presentations/packaging/#slide:1
https://svn.python.org/projects/sandbox/trunk/setuptools/setuptools.txt

# Steps

## 新建一个项目

```
Example1/
|-- setup.py
|-- submodule1/
|   |-- __init__.py
|   |-- tests
...
|-- submodule2/
|   |-- __init__.py
|   |-- tests
|-- support_files
|   |-- ...
...
```

## 版本

版本的格式：

* Python 的版本号格式为 `<version<.pre-release>>.<build>.<post-release>`。各小节之间用 `.` 来分割，切记不要使用 `-` 例如：`0.0.1`; `2.4`；`1.0.2.a1.dev.r100`。
* 每个小节都是可选的，不需要完整表述。
* 预览标记 pre-release 约定：`a` 表示 Alpha，`b` 表示Beta，`rc` 表示 release candidate，rc 也可以写成 `c` 或 `pre` 或 `preview`。
* 以上预览版本标记 (pre-release）标记后面可以跟一个数字，并且和版本号之间可以不需要`.`隔开。比如这些都是合法的预览版本： `0.0.1a1`；`2.4c100` 等。
* 在版本和后缀(post-release)之间还可以添加一些构建标记，比如 build number 或环境标示等： `0.0.1a1.dev0`；`2.4b1.dev0.20201119`; `2.4.b1.dev0.rc1`。注意：`2.4b1.dev0.20201119 的版本比 2.4b1.dev0 新`
* 任意小节如果以数字结尾，则和后面的小节之间不使用 `.` 分割：`0.0.1a0dev0` 等同于 `0.0.1a0.dev0`，也等同于 `0.0.1.a.dev0`；但是不等同于 `0.0.1adev0`
* 数字 0 可以缺失。
* 字符串参与版本之间的比较，比如：`0.0.1dev1 > 0.0.1a1 > 0.0.1aev1`
* `+` 是合法的版本字符，不是分割符，但是在比较中它比 `a` 还小，而 `a` 比 `0` 小。

以下命令可以用来检查版本格式和比较新旧:

```python
from pkg_resources import parse_version
# 可以省略数字
parse_version('1.9.a.dev') == parse_version('1.9a0dev')    # True
# `-` 是遗留标示，建议用 `.` 代替
parse_version('2.1-rc2') == parse_version('2.1.rc2')            # True
parse_version('0.6a9dev0.r41475') < parse_version('0.6a9')  # True
# 数字结尾无需 `.` 分割
parse_version('0.6a0dev0r41475') == parse_version('0.6a.dev.r41475')  # True
# 有 post-release 标示大于没有
parse_version('0.6a9dev0.r41475') < parse_version('0.6a9dev0')  # True
# 数字按大小排序 
parse_version('0.6a9dev0.r41475') < parse_version('0.6a9dev0.r41474')   # False
parse_version('0.6a9.dev0.r41475') < parse_version('0.6a9.dev0.r41476')   # True
# a == a0 > aa
parse_version('0.0.1.aa') < parse_version('0.0.1.a')          # True
# `+` 最小
parse_version('0.0.1.a+') < parse_version('0.0.1.a')          # True
# 纯净的版本号小于 r(release)，大于其它。注意 r 不等于 rc，rc 标示预览，在排序上没有优势。
parse_version('0.0.1.r') > parse_version('0.0.1')          # True
parse_version('0.0.1.b') < parse_version('0.0.1')          # False
```

有两种方式获得版本

1. （推荐）显式指定版本：
在项目中定义个版本文件 __VERSION__.py 或者直接在 __init__.py 中设置版本变量，变量名任意，比如 `__version__="0.0.1"`，然后在 setup.py 中引入：

```
version=__init__.__version__,
```

2. （不推荐）根据 git revision number(和 tag number) 来自动生成版本号
需要安装 `setuptools`　和　`setuptools-version-command`

```
$ pip install setuptools　setuptools-version-command
```

`setuptools-version-command` 用于实现动态版本控制(https://pypi.python.org/pypi/setuptools-version-command/1.3.5)，
然后根据 revision number（需要 check in git 以获得 revision number）

```
version_command='git describe --always --tags --long --dirty=.dev'
```

如果不想借助 setuptools-version-command，也可以通过以下命令获得：

```python
def get_version(): 
    import subprocess
    return subprocess.check_output(['git', 'describe', '--always', '--tags', '--long', '--dirty=.dev']).decode('ascii').strip()
```

3. 但是请注意，以上方式得到的版本标示不是标准的，因此不推荐。但是可以通过以下方式定制合法格式，需要安装 `setuptools-git-version` 包来支持：

```
version_format='{tag}.dev{commitcount}+{gitsha}',
setup_requires=['setuptools-git-version'],
```

这种方式必须对项目打 tag

不同的版本获取命令，对应不同的版本管理方式，对打包命令的使用也会产生不同的要求。

## 在项目根目录下执行 `setuptools`！！

注意，因为这个项目包含多个 Example，每个都是一个独立的根项目，所以运行其中的测试案例的时候需要将执行目录切换到相应的案例根目录下，否则会报告模块找不到。
Python 项目的打包方式有多种，先查看一下打包内容：

```bash
$ python setup.py egg_info
```

### 推荐打包 wheel 格式发布文件。以`显式指定版本`为例：

`显式指定版本`方式下缺省的打包命令将直接生成带版本号的包：

如果是开发版：

```bash
$ python setup.py egg_info -bDEV -d bdist_wheel   # 推荐
```

`-bDEV` 为可选参数。在该方式下它会为打包出来的文件自动匹配后缀，比如 `0.0.1.dev0...`，`version.dev0` 是 python 打包文件的标准版本格式。其中：

* `dev`：表示开发版，由 `-b` 或 `--tag-build` 来指定。`0`是自动添加的 commit 次数，有时候我们希望用其它数字代替，比如打包日期，可以使用 `--tag-date`
或 `-d` 将其替换成日期。

`根据 git revision 自动生成版本` 方式下，无需使用`-b` 参数。`version` 将根据命令格式自动生成。

### 或打包 egg 格式发布文件

```bash
$ python setup.py bdist_egg
```

### 打包源代码, 这将打包所有文件

```bash
$ python setup.py sdist
```

输出一些新的文件:

```
Example1
|-- mymodules.egg-info
|   |-- dependency_links.txt
|   |-- ...
|-- dist
|   |-- mymodules-0.0.2-3-g92ad88d-dev.tar.gz
|-- build       # (sdist不会生成这个目录)
|   |-- bdist.linux-x86_64/
|   |-- lib/...
|-- setup.py
|-- MANIFEST.in
```

* `bdist_egg`　参数将生成 `mymodules-0.1-py3.6.egg` 取代 `mymodules-0.1-py3.6.tar.gz` (不推荐)

### dist  下的文件就是发布包，可以用 `unzip` 来察看内容：

```
$ upzip -l dist/mymodules-0.1-py3.6.tar.gz
Archive:  dist/mymodules-0.1-py3.6.tar.gz
  Length      Date    Time    Name
---------  ---------- -----   ----
        1  2013-06-07 22:03   EGG-INFO/dependency_links.txt
        1  2013-06-07 22:03   EGG-INFO/zip-safe
      120  2013-06-07 22:03   EGG-INFO/SOURCES.txt
        1  2013-06-07 22:03   EGG-INFO/top_level.txt
      176  2013-06-07 22:03   EGG-INFO/PKG-INFO
       95  2013-06-07 22:21   submodule1/__init__.py
      338  2013-06-07 22:23   submodule2/__init__.pyc
      ...
```

## 单元测试

在项目下新建 tests　单元测试目录，并新建一个 `__init__.py` 文件内容可以为空，如果没有 `__init__.py`，setuptools 将忽略该目录。
编写测试文件然后执行单元测试：

```
$ python setup.py test
...
running build_ext
test_hello (submodule1.tests.test_cases.TestJoke) ... ok
...
test_hello (submodule2.tests.test_cases.TestJoke) ... ok
...
```
https://docs.python.org/2/library/unittest.html

## 安装

在项目根目录下子执行安装：

```
python -m pip install dist\mymodules-0.0.2_3_g92ad88d-py3.6.tar.gz
```

或

```
python -m easy_install dist\mymodules-0.0.2_3_g92ad88d-py3.6.egg
```

或从头连编译打包带安装:

```
$ python setup.py install
```

项目将会被安装到系统的 `/usr/local/lib/python3.6/dist-packages`　目录下并允许被其他项目引用:

```
import submodule1
submodule1.hello()
```

Windows 被安装到 `c:\program files\python\python36\lib\site-packages`目录

## 反安装

```
pip uninstall mymodules
```

# 发布

```
python setup.py bdist_wheel bdist_wininst upload -r http://example.com/pypi
```

# 执行
`__main__.py` 是外部入口，它不能在模块被安装前直接执行，因为它尝试如同第三方程序载入模块然后执行它。

```
$ python -m submodule1
```

这将导致 python 尝试从 `__main__.py` 执行 `submodule1.init()` 也就是执行 `submodule1.__init__.init()`

# Release

在 home 目录下配置.pypirc 文件：(假设 pypi 地址为：https://www.xxx.com/artifactory/pypi/simple/)

```
[distutils]
index-servers = local
[local]
repository: https://www.xxx.com/artifactory/pypi
username: <USERNAME>
password: <PASSWORD>
```

1) 发布

```
# python setup.py bdist_wheel upload -r local
```

2) twine

```bash
# pip install twine
```

```bash
# twine upload --repository local --cert=/path/to/certification dist/*
或
# twine upload --repository-url https://www.xxx.com/artifactory/pypi --cert=/path/to/certification dist/*
```
