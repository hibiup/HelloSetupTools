https://blog.ionelmc.ro/presentations/packaging/#slide:1

# Steps

## 安装 `setuptools`　和　`setuptools-version-command`

```
$ pip install setuptools　setuptools-version-command
```

`setuptools-version-command` 用于实现动态版本控制(https://pypi.python.org/pypi/setuptools-version-command/1.3.5)，可以通过　`python setup.py --version` 获得版本号并传递给 git，同时使得可以在 `setup.py` 中使用 `version_command` 指令。

```
$ git tag -a $(python setup.py --version)-dev -m 'description of version'
```

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

## 在项目根目录下执行 `setuptools`！！

注意，因为这个项目包含多个 Example，每个都是一个独立的根项目，所以运行其中的测试案例的时候需要将执行目录切换到相应的案例根目录下，否则会报告模块找不到。

```
$ python setup.py sdist   # 推荐
```
或

```
$ python setup.py bdist_egg
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
python setup.py sdist bdist_wininst upload -r http://example.com/pypi
```

# 执行
`__main__.py` 是外部入口，它不能在模块被安装前直接执行，因为它尝试如同第三方程序载入模块然后执行它。

```
$ python -m submodule1
```

这将导致 python 尝试从 `__main__.py` 执行 `submodule1.init()` 也就是执行 `submodule1.__init__.init()`