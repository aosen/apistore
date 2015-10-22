# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options

import routers.urls
from settings import TEMPLATE_PATH, STATIC_PATH, DEBUG

from tornado.options import define, options
define("host", default="127.0.0.1", help="run on the given host", type=str)
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = routers.urls.urlpatterns
        settings = dict(
                template_path=TEMPLATE_PATH,
                static_path=STATIC_PATH,
                debug=DEBUG,
                )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address=options.host)
    tornado.ioloop.IOLoop.instance().start()
