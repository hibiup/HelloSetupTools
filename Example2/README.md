# 依赖管理

`autoupgrade` 包提供了自动依赖检查，可以让 submodule2 在安装前检查依赖的 submodule1 的版本，并自动升级到最新版。但是 test 执行在 setup 之前，因此 autoupgrade 包本身无法被自动安装，需要手工安装。安装命令是:

```
$ pip install https://bitbucket.org/jorkar/autoupgrade/get/master.tar.gz
```
## AutoUpgrade

`autoupgrade.AutoUpgrade` 可以指向内部  `pypi`，只需指定 `index` 参数即可：

```
from autoupgrade import AutoUpgrade
AutoUpgrade("submodule1", index="https://pypi.company.com/repos").upgrade_if_needed()
```

当然，我们需要将 submodule1 在发布的时候 `upload` 到这个 `pypi` 上去。

## git+https

依赖管理中另外一个蛋疼得问题是 `setup.install_requires` 不支持 url，因此如果当 `requirements.txt` 文件存在以下内容时会失败。
```
git+https://git.company.com/Example1.git@master#egg=submodule1-0.0.2
```
格式：
* git+http(s) 或 git+ssh 开头
* @\<branch>
* #\<packagename>-\<version>

所以需要将它分开处理，将url交给 `dependency_links`（但是安装的时候 pip 会忽略 `dependency_links` ），因此最好的做法还是应该将 submodule1 在发布的时候上载到 pypi.