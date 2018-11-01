# -*- coding: utf-8 -*-
'''数据库迁移配置'''
from flask_script import Manager
from flask_migrate import (
    Migrate,
    MigrateCommand
)

from run import start_server


if __name__ == '__main__':
    app = start_server(is_deploy=True)
    migrate = Migrate(app, app.db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()