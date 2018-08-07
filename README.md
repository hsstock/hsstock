# Quantum Exchange

## Python 工程化
这篇文章中主要涉及下面几点，都是我以为的工程化必须谈到的几个问题：
- 项目架构，目录组织结构
- 代码规约，linter 相关
- 测试
- 日志系统
- 构建 / 发布 / 部署


## pyhon 目录结构
懒得看的话直接参考这个 [sample 项目A](https://github.com/kennethreitz/samplemod)，或者这一个 [sample 项目B](https://github.com/pypa/sampleproject)。

python 作为一门讲究规约 (convention) 的语言，在项目结构上可参考 python 两个应用最广泛的 Web 框架：
- [django](https://github.com/django/django)，django 作为一个功能完备的 Web  框架，在其项目结构中，业务代码都集中在 `/django` 文件夹中。
- [flask](https://github.com/pallets/flask), flask 比起 django 更精简，业务代码在 `/flask` 文件夹中，里面甚至没有更深一层的模块分层，每个功能都按 `.py` 文件组织。

### 举个简单例子
```
Foo(项目名)/
|-- bin/
|   |-- foo
|
|-- foo(小写项目名)/
|   |-- package/
|   |   |-- __init__.py
|   |   |-- module.py
|   |
|   |-- __init__.py
|   |-- main.py
|
|-- tests/
|   |-- package/
|   |   |-- __init__.py
|   |   |-- test_main.py
|   |
|   |-- __init__.py
|   |-- main.py
|
|-- docs/
|   |-- conf.py
|   |-- abc.rst
|-- data/
|-- Dockerfile
|-- setup.py
|-- requirements.txt
|-- README.md
|-- CHANGELOG.txt
|-- LICENSE
|-- MANIFEST.in
```
简要解释一下:

- bin/: 存放项目的一些可执行文件，当然你可以起名script/之类的也行。
- foo/: 存放项目的所有源代码。
    1. 源代码中的所有模块、包都应该放在此目录。不要置于顶层目录。
    2. 程序的入口最好命名为 `main.py`。
- test/: 存放单元测试代码，跟源代码目录结构一致，测试文件名规则: "test_" + moduleName
- docs/: 存放一些文档。
- data/: 存放数据。
- Dockerfile: 镜像制作模板
- `setup.py`: 安装、部署、打包的脚本。
- requirements.txt: 存放软件依赖的外部Python包列表。
- README: 项目说明文件。
- CHANGELOG: 代码维护说明日志。
- LICENSE: 版权说明。
- MANIFEST.in: 文件清单。


Ref:
- [创建高质量Python工程(1)-如何设计结构清晰的目录结构](http://monklof.com/post/19/)
- [结构化您的工程](http://pythonguidecn.readthedocs.io/zh/latest/writing/structure.html)

## 构建 / 发布 / 部署
### 虚拟环境
这里安装、构建项目的一个前提是，建立在虚拟环境上，无论是 [venv](https://docs.python.org/3/library/venv.html#module-venv)/[Virtualenv](https://virtualenv.pypa.io/en/stable/) 还是 [Conda](https://conda.io/docs/user-guide/overview.html)。这里假设这是一个普通的 python 项目(非大数据项目)，且不需要支持 python 2.X，虚拟环境选择 venv。
#### 命令行构建虚拟环境
运行一下命令安装虚拟环境：`python3 -m venv /path/to/new/virtual/environment`
虚拟环境安装后，会在项目目录下，创建一下文件（夹）：
- bin
- include
- lib
- pyvenv.cfg
- share

具体文件夹根据不同的系统会有所差别，上面仅以 Linux 为例。在 `/lib/pyhonX.Y/site-packages` 中能找到几个默认安装的包：
- pip
- setuptools
##### 激活虚拟环境
依然以 Linux 为例，运行下面命令：
`source <venv>/bin/activate`
激活虚拟环境后，使用 `pip` 安装依赖时，`pip` 便会自动把依赖安装到 `/lib/pyhonX.Y/site-packages` 中。
##### 确认激活
运行下面命令：`which pyhon`，若位于项目目录中，激活成功。

#### pyCharm 建立虚拟环境
点击在目录菜单 `File`，依次选择 `Settings` -> `Project Interpreter`，然后点击 Project Interpreter 右手边的配置按钮，选择 `Add Local ...`，在 `Virtualenv Environment` 这栏中的 `Base interpreter` 中选择上面 `python 3` 安装目录。
具体步骤可参考 pyCharm Help [这个页面](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html)。

若使用 pyCharm （2017 之后版本）的话，在 `Settings -> Tool -> Terminal` 选项中默认是勾上 Activate virtualenv 选项的。此时在 pyCharm 中的 Terminal 使用 pip install 默认就是安装在虚拟环境中了。

### 安装构建
#### setup.py & setuptools
在上面章节`pyhon 目录结构`中，可在根目录下找到 setup.py 文件。setup.py 有两个功能：
1. 通过 setup() 方法描述项目，类似 Maven 中的 pom.xml 或 JS 项目中的 package.json，方法参数见这个[链接](https://packaging.python.org/tutorials/distributing-packages/#setup-args)，建议大致看看里面的参数；
2. 构建项目的命令行接口（还包括其他的命令，可通过 `python setup.py --help-commands` 来获取帮助，这个[链接](https://pythonhosted.org/an_example_pypi_project/setuptools.html)中的 Using setup.py 章节也有介绍）。

在当前版本的 python(python 3.6) 中，推荐在 setup.py 中使用 [setuptools](https://setuptools.readthedocs.io/en/latest/)。在旧版本中 (python 2.4 或以前) 是推荐使用 disutils 这个包的，见这份 [legacy 文档](https://docs.python.org/3/install/index.html)。

setup.py 的编写可参考下面两个例子：
- [解释详尽的例子](https://github.com/pypa/sampleproject/blob/master/setup.py)
- [简单例子](https://github.com/kennethreitz/samplemod/blob/master/setup.py)

#### 安装依赖
在 setup.py 中确定, 打包命令: python setup.py sdist, 生成dist和(setup.name).egg-info目录。

```
#This archive can be used directly with PIP to install the project as follows
pip install dist/***-version.tat.gz

```

#### 配置中心

- 配置HOST
    - 10.173.34.14 apollo-configservice-dev.dev-pbim-space-cnpbimserver.svc.cluster.local
    - 10.173.34.76 apollo-configservice-fat.test-pbim-cnpbimserver.svc.cluster.local
    - 10.173.34.79 apollo-configservice-uat.pre-pbim-cnpbimserver.svc.cluster.local
    - 10.173.34.8 apollo-configservice-pro.prod-pbim-cnpbimserver.svc.cluster.local
- 环境变量
    - DEV 开发环境
    - FAT 测试环境
    - UAT 预发布环境
    - PRO 线上环境
 - 设置环境变量
    启动时添加 `ENV = DEV` 的环境变量即可
 - PORTAL管理
    - 地址： http://10.173.34.20:8080/config.html#/appid=aiar
    - 权限：如无权限联系徐立果添加
 - 使用示例
 ```
 from aiar.apollo.config_service import ConfigService

 #defaultValue可省略
 value = ConfigService.appConfig().get_value("key", "defaultValue")
 print(value)
 ```
 
#### Docker镜像制作

- 镜像制作命令
```
docker build -t hub.c.163.com/cnpbimserver/hsqe:d-0.0.1 .
```
- 启动容器
```
docker run -p 8888:8888 -it --rm --name crawler  hub.c.163.com/cnpbimserver/hsqe-b:d-0.0.1
```

## 代码规约
### Python 风格指南
见这个[链接](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/#)
### Pylint
使用 [Pylint](https://pylint.readthedocs.io/en/latest/) 对代码进行静态检查。
#### 在 PyCharm 中使用 Pylint
1. 在系统中全局安装 Pylint：`pip install pylint`
2. 在 PyCharm 中添加 Pylint: `File -> Settings -> Tools -> External Tools`
    - 点击页面右半部的小加号
    - 在新弹窗填写：
        - Name: Pylint
        - Program: Pylint 的安装目录，Linux 下可用命令 `which pylint` 获取
        - Parameters: $FilePath$ --rcfile=$ProjectFileDir$\.pylintrc，--rcfile 指定自定义的 linter 规则
        - Working Directory: $ProjectFileDir$
 3. 添加完成后：
     - 在菜单栏点击 `Tools -> External Tools -> Pylint`，linter 当前文件；
     - 项目目录结构中，右键 `External Tools -> Pylint`，linter 项目。

Ref: [pylint-in-pycharm](https://pylint.readthedocs.io/en/latest/user_guide/ide-integration.html#pylint-in-pycharm)
##### Pylint 的 MESSAGE_TYPE：
- (C) 惯例。违反了编码风格标准
- (R) 重构。写得非常糟糕的代码。
- (W) 警告。某些 Python 特定的问题。
- (E) 错误。很可能是代码中的错误。
- (F) 致命错误。阻止 Pylint 进一步运行的错误

Ref: [如何使用 Pylint 来规范 Python 代码风格](https://www.ibm.com/developerworks/cn/linux/l-cn-pylint/index.html)

#### [接口描述](https://futunnopen.github.io/futuquant/api/Market_API_Python_Doc.html#)

#### [unittest](https://docs.python.org/3/library/unittest.html)

Note that the order in which the various test cases will be run is determined by sorting the test function names with respect to the built-in ordering for strings.

#### [ThirdParty Source Code](/Users/hujiabao/anaconda3/lib/python3.6/site-packages)

/Users/hujiabao/anaconda2/lib/python2.7/site-packages/vnpy/

#### Upgrade  pip2.7

```
curl -0 https://bootstrap.pypa.io/get-pip.py >> get-pip.py
sudo python2.7 get-pip.py
```
```
cp -rf /Users/hujiabao/anaconda3/lib/python3.6/site-packages/talib /Users/hujiabao/anaconda2/lib/python2.7/site-packages/
cp -rf /Users/hujiabao/anaconda3/lib/python3.6/site-packages/futuquant /Users/hujiabao/anaconda2/lib/python2.7/site-packages/
cp -rf /Users/hujiabao/anaconda3/lib/python3.6/site-packages/vnpy /Users/hujiabao/anaconda2/lib/python2.7/site-packages/

conda install -c quantopian ta-lib
conda install -c quantopian/label/pandas_upgrade ta-lib
```
#### 升级OSX High Sierra 10.13遇到一些问题及解决方法

[升级OSX High Sierra 10.13遇到一些问题及解决方法](https://blog.csdn.net/jackymvc/article/details/78256120)

#### 安装第三方软件

```
brew install zmq
```

[tushare](http://tushare.org/)

[SQLAlchemy](http://docs.sqlalchemy.org/en/latest/orm/query.html)

[SQLAlchemy Paginate](https://www.cnblogs.com/rgcLOVEyaya/p/RGC_LOVE_YAYA_350days.html)
[MySQL Config](https://www.cnblogs.com/zengkefu/p/5634858.html)
[MySQL QueryCache](https://blog.csdn.net/qq_27238185/article/details/54096069)

[APM](https://docs.newrelic.com/docs/agents/python-agent/getting-started/instrumented-python-packages)

#### [Python教程](http://www.runoob.com/python3/python3-built-in-functions.html)

[sqlalchemy](https://www.sqlalchemy.org/)


#### Tushare

1. "ts_" as the table prefix for tushare server


#### Code Piece

1.

```
        # try:
        #     logging.info("test change field type,  starting")
        #
        #     df = pd.DataFrame({'A': ['-', '1.0'], 'B': ['-', '-']})
        #     # df['A'][0] = 1
        #     df = change_df_filed_type(df, ['A', 'B'], float, '-', 0.0)
        #     table = 'aaaaa'
        #     storeservice.insert_many(table, df)
        #     logging.info("test change field type, end")
        # except IOError as err:
        #     logging.error("OS|error: {0}".format(err))
        # else:
        #     print('success')
```

2. 多线程，网络不稳定，服务器不可控
```
# class Thread_get_today_all (threading.Thread):
#     def __init__(self, threadname,ts):
#         threading.Thread.__init__(self)
#         self.threadname = threadname
#         self.ts = ts
#
#     def run(self):
#         logging.info ("开始线程：" + self.threadname)
#         self.ts.get_today_all()
#         logging.info ("退出线程：" + self.threadname)
#
 # tfn_get_today_all = Thread_get_today_all('tfn_get_today_all',ts)
    # tfn_get_today_all.start()
    # tfn_get_today_all.join()

```

3.
```
df = df.replace('', 0)
df['buy'] = df['buy'].astype(float)

df['code'] = df['code'].map(lambda x: str(x).zfill(6))
df = df.drop_duplicates('code')
```
4.
```
def _cap_tops(last=5, pageNo=1, retry_count=3, pause=0.001, dataArr=pd.DataFrame()):
    ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(rv.LHB_SINA_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], rv.LHB_KINDS[0],
                                               ct.PAGES['fd'], last, pageNo))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table[@id=\"dataTable\"]/tr")
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df.columns = rv.LHB_GGTJ_COLS
            dataArr = dataArr.append(df, ignore_index=True)
            nextPage = html.xpath('//div[@class=\"pages\"]/a[last()]/@onclick')
            if len(nextPage)>0:
                pageNo = re.findall(r'\d+', nextPage[0])[0]
                return _cap_tops(last, pageNo, retry_count, pause, dataArr)
            else:
                return dataArr
        except Exception as e:
            print(e)

```
5.
```
kill -9 $(ps aux | grep python | awk '{print $2}')
```
#### 数据资产

[通联数据](https://app.wmcloud.com/cloud-portal/#/portal)
