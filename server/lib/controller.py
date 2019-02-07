#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.server import Server
from lib.operational.bhash import BHash

class Controller(Server):
    name = 'Controller'
    bhash = BHash()

    def GET(self, pathinfo):
        return self.render.index(
            self.bhash.hotTags(),
            self.bhash.lastTags(),
            self.bhash.trendTags()
        )
