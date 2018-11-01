# -*- coding: utf-8 -*-
'''测试阶段-启动文件'''
import os

from werkzeug.routing import EndpointPrefix

from backend.startup import create_app
from backend.utils import touch


def get_site_version(root):
    '''获取网站版本'''
    vf = os.path.join(root, 'site.version')
    if not os.path.exists(vf):
        touch(vf)
    v = None
    with open(vf, 'r') as f:
        v = f.read().strip()
        if not bool(v):
            v = '0.0.0'
    return v

def start_server(run_cfg={}, is_deploy=False):
    '''启动web服务器'''
    proj_root = os.path.abspath(os.path.dirname(__file__))
    os.environ['PROJ_ROOT'] = proj_root
    site_version = get_site_version(proj_root)
    os.environ['SITE_VERSION'] = site_version
    config = {
        'use_cdn': True,
        'debug': run_cfg.get('debug', False),
        'secret': '!secret!',
        'url_prefix': None
    }
    app = create_app(config)
    app.proj_root = proj_root
    app.site_version = site_version

    @app.before_first_request
    def init_staff(*args, **kwargs):
        print(args)
        print(kwargs)
        with app.app_context():
            from backend.admin.models import Staff

            db = app.db

            if Staff.query.filter_by(name='admin').count() < 1:
                staff_obj = Staff()
                staff_obj.name = 'admin'
                staff_obj.email = 'admin@gsw945.com'
                staff_obj.password = Staff.encrypt_string('administrator')
                staff_obj.is_admin = True
                db.session.add(staff_obj)
                db.session.commit()
                print('添加初始数据成功')
            else:
                staff_obj = Staff.query.first().to_dict()
            if isinstance(staff_obj, Staff):
                print(staff_obj)

    if is_deploy:
        return app
    app.run(**run_cfg)

if __name__ == '__main__':
    run_cfg = {
        'host': '0.0.0.0',
        'port': 5556,
        'debug': False,
        'threaded': True
    }
    start_server(run_cfg)