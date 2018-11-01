# Flask-Bigger *Flask大型应用骨架*

## 后端说明
> 使用 **Python 3** (理论上 **Python 2**可以正常运行，但是未测试)

### 后端-使用的第三方库
* **Flask**
    - [GitHub](https://github.com/pallets/flask)
    - [PyPi](https://pypi.python.org/pypi/Flask)
    - [Doc](http://flask.pocoo.org/docs/)
    - [Doc-v0.10](http://docs.jinkan.org/docs/flask/)(中文)
    - [Doc-v0.11](http://python.usyiyi.cn/translate/flask_011_ch/index.html)(中文)
* **Jinja2**
    - [GitHub](http://github.com/mitsuhiko/jinja2)
    - [PyPi](https://pypi.python.org/pypi/Jinja2)
    - [Doc](http://jinja.pocoo.org/docs/)
    - [Doc](http://python.usyiyi.cn/translate/jinja2_29/index.html)(中文)

### 安装依赖包
```shell
pip install -r requirements.txt
```

### 数据库迁移
1. 初始化迁移配置
    ```shell
    python manage.py db init
    ```
2. 生成迁移文件
    ```shell
    python manage.py db migrate
    ```
3. 执行迁移操作(更改到数据库)
    ```shell
    python manage.py db upgrade
    ```
4. 查看帮助
    ```shell
    python manage.py db --help
    ```

### 安装依赖包
```shell
pip install -r requirements.txt
```

### 开发运行
```shell
python ./run.py
# 或者
python manage.py runserver --host 0.0.0.0 --port 5555
```

---

## 前端说明

### 前端-使用的第三方库
* **Bootstrap**
    - [GitHub](https://github.com/twbs/bootstrap)
    - [Doc-com](http://getbootstrap.com)
    - [Doc](https://v3.bootcss.com)(中文)

## (关键)目录、文件说明
```
├── backend                     # 后端文件目录
│   ├── admin                   # 子应用目录
│   |   ├── __init__.py         # admin子应用-公共文件(和包入口)
│   |   ├── main.py             # admin子应用-核心路由(用户系统)
│   |   ├── models.py           # admin子应用-模型
│   │   ├── secure.py           # admin子应用-安全访问控制
│   │   └── views               # admin子应用-业务视图
│   ├── app_env.py              # 应用环境变量配置获取
│   ├── app_map.py              # 子应用入口
│   ├── apps                    # 子应用目录
│   |   ├── ...                 # 各子应用
│   │   └── __init__.py         # 子应用公共文件(和包入口)
│   ├── core                    # 站点核心(独立于具体业务)文件目录
│   ├── startup.py              # 站点启动入口文件
│   └── utils.py                # 工具库
├── deploy.py                   # 部署-启动文件
├── frontend                    # 文件目录
│   ├── static                  # 静态文件目录
│   |   ├── ...                 # 自定义静态文件
|   │   ├── favicon.ico         # 站点图标
|   │   ├── robots.txt          # 搜索引擎配置文件
│   |   └── _libs               # 第三方库
│   └── templates               # 模板目录
│       ├── ...                 # 各子应用模板
│       └── base-layout.html    # 基础父模板
├── README.md                   # 项目说明
├── requirements.txt            # 依赖包清单文件
├── run.py                      # 开发运行-启动文件
└── site.version                # 站点版本文件
```