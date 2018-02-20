# Steps

## 安装 `setuptools`　和　`setuptools-version-command`
```
$ pip install setuptools　setuptools-version-command
```

`setuptools-version-command` 用于实现动态版本控制(https://pypi.python.org/pypi/setuptools-version-command/1.3.5)，可以通过　`python setup.py --version` 获得版本号并传递给 git:

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
...
```

## 在项目根目录下执行 `setuptools`
```
$ python setup.py bdist_egg
```

输出一些新的文件:
```
Example1
|-- build
|   |-- bdist.linux-x86_64/
|   |-- lib/...
|-- mymodules.egg-info
|   |-- dependency_links.txt
|   |-- PKG-INFO
|   |-- SOURCES.txt
|   |-- top_level.txt
|-- dist
|   |-- mymodules-0.1-py3.6.egg
|-- setup.py
```

### dist  下的 `egg` 文件就是发布包，可以用 `unzip` 来察看内容：
```
$ upzip -l dist/mymodules-0.1-py3.6.egg
Archive:  dist/mymodules-0.1-py3.6.egg
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

## 安装

在项目根目录下子执行安装：
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