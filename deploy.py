# -*- coding: utf-8 -*-
'''部署阶段-启动文件'''
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from run import start_server


if __name__ == '__main__':
    wsgi_app = start_server(is_deploy=True)
    host = '0.0.0.0'
    port = 5555
    print('visit by [http://{0}:{1}/]'.format(host, port))
    http_server = HTTPServer(WSGIContainer(wsgi_app))
    http_server.listen(port, address=host)

    IOLoop.instance().start()