import web
from lib.utils.webu import WebUtility


class Server(WebUtility):
    render = web.template.render('templates')


class HttpStatus(web.HTTPError):
    def __init__(self, level, message=None):
        status = '%d Error %s' % (level, message)
        headers = {'Content-Type': 'text/html'}
        data = '<h1>%s</h1>' % status
        web.HTTPError.__init__(self, status, headers, data)

