#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import web
from lib.controller import Controller
from lib.service import Service
from etc.config import Config


class Debug:

    def GET(self, pathinfo):
        return "a DEBUG patch @ {}".format(Service.__name__)


web.config.debug = False
web.config.session_parameters['secret_key'] = Config.secret

urls = (
        Config.urlPrefix + '/s/(.*)$', Service.__name__,
        Config.urlPrefix + '/(.*)$', Controller.__name__,
        "(/.*)", "Debug"
        )

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'auth': False})

if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()