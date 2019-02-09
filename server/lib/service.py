import web
from etc.config import Config
from lib.utils.webu import WebUtility
from lib.operational.bhash import BHash
from lib.server import HttpStatus
from lib.exceptions import AuthException
import json


class Service(WebUtility):
    name = 'Service'
    bHash = BHash()

    def asJson(self, payload, container=None):
        return json.dumps(payload if container is None else {container: payload})

    def setResultLimit(self, argument):
        try:
            return int(argument)
        except:
            return Config.defaultResultLimit

    def getResults(self, func, pathinfo, args):
        args.setdefault('limit', self.setResultLimit(
            pathinfo[0] if len(pathinfo) > 0 else Config.defaultResultLimit))
        return func(args.get('limit'))

    def hotTags(self, pathinfo, args):
        return self.getResults(self.bHash.hotTags, pathinfo, args)

    def lastTags(self, pathinfo, args):
        return self.getResults(self.bHash.lastTags, pathinfo, args)

    def trendTags(self, pathinfo, args):
        return self.getResults(self.bHash.trendTags, pathinfo, args)

    def byUser(self, pathinfo, args):
        args.setdefault('limit', self.setResultLimit(pathinfo[1]) if len(pathinfo) > 1 else Config.defaultResultLimit)
        args.setdefault('uid' if pathinfo[0].isnumeric() else 'username', pathinfo[0] if len(pathinfo) > 0 else None)
        args.setdefault('uid')
        args.setdefault('username')
        return self.asJson(self.bHash.byUser(args.get('uid'), args.get('username'), args.get('limit')), 'items')

    def byTime(self, pathinfo, args):
        args.setdefault('limit', self.setResultLimit(pathinfo[0]) if len(pathinfo) > 0 else Config.defaultResultLimit)
        return self.asJson(self.bHash.byTime(args.get('limit')), 'items')

    def byTag(self, pathinfo, args):
        args.setdefault('tag', pathinfo[0] if len(pathinfo) > 0 else None)
        args.setdefault('limit', self.setResultLimit(pathinfo[1]) if len(pathinfo) > 1 else Config.defaultResultLimit)
        return self.asJson(self.bHash.byTag(args.get('tag'), args.get('limit')), 'items')

    def byId(self, pathinfo, args):
        if len(pathinfo) > 0:
            args.setdefault('id', pathinfo[0])
        return self.bHash.byId(args.get('id'))

    def register(self, pathinfo, args):
        if len(args) == 0:
            args = self.gerarchyInterpreter(pathinfo, ('username', 'password', 'email'))

        self.bHash.register(args.get('username'), args.get('password'), args.get('email', None))
        return 'User %s saved' % args.get('username')

    def token(self, pathinfo, args):
        if len(args) == 0:
            args = self.gerarchyInterpreter(pathinfo, ('username', 'password', 'duration'))
        args.setdefault('duration', None)
        try:
            return self.bHash.token(args.get('username'), args.get('password'), args.get('duration'))
        except AuthException as e:
            raise HttpStatus(403, e)
        except:
            raise HttpStatus(403, 'Auth failed')

    def publish(self, pathinfo, args):
        if len(pathinfo) > 0:
            args.setdefault('token', pathinfo[0])
        try:
            return self.bHash.publish(args.get('token'), args.get('content'), args.get('tags'))
        except AuthException as e:
            raise HttpStatus(403, e)
        except Exception as e:
            raise HttpStatus(500, e)

    def GET(self, pathinfo):
        return self.controller(pathinfo, {})

    def POST(self, pathinfo):
        return self.controller(pathinfo, web.input())

    def controller(self, pathinfo, args):
        pi = self.getOp(pathinfo)
        try:
            method = getattr(type(self), pi[0])
            return method(self, args=args, pathinfo=pi[1-len(pi):])
        except AuthException as e:
            raise HttpStatus(403, '{}'.format(e))
        except AttributeError:
            raise HttpStatus(404, 'Unsupported Operation {}'.format(pi[0]))
        except Exception as e:
            raise HttpStatus(500, e)
