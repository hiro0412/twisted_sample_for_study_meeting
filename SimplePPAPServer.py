"""Simple PPAP Server.
"""


__version__ = "0.1"


import BaseHTTPServer
from SocketServer import ThreadingMixIn
import sys
import shutil
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import random
from time import sleep
import re

SLEEPTIME=3

items = ['Pen', 'Apple', 'Pineapple']
goods = dict()
messages = []

random.seed()
for i in range(10):
    elements = []
    num = int(random.random() * 4) + 1
    for j in range(num):
        elements.append(items[int(random.random() * len(items))])
    key = ''.join(elements)
    goods[key] = elements
    messages.append('I have a ' + key)


class ThreadingHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


class SimplePPAPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "SimplePPAP/" + __version__

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            try:
                shutil.copyfileobj(f, self.wfile)
            finally:
                f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        path = self.path[1:]
        if re.match('^\d+$', path):
            try:
                index = int(path)
            except ValueError:
                self.send_error(404, "invalid path")
                return None
            else:
                return self.gen_message(index)
        else:
            return self.gen_goods(path)


    def gen_message(self, index):
        sleep(SLEEPTIME)
        if index < len(messages):
            f = StringIO()
            f.write(messages[index])
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            encoding = sys.getfilesystemencoding()
            self.send_header("Content-type", "text/html; charset=%s" % encoding)
            self.send_header("Content-Length", str(length))
            self.end_headers()
            return f            
        else:
            self.send_error(404, "index error.")
            return None


    def gen_goods(self, key):
        sleep(SLEEPTIME)
        if key in goods:
            f = StringIO()
            f.write(repr(goods[key]))
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            encoding = sys.getfilesystemencoding()
            self.send_header("Content-type", "text/html; charset=%s" % encoding)
            self.send_header("Content-Length", str(length))
            self.end_headers()
            return f            
        else:
            self.send_error(404, "invalid path")
            return None


def test(HandlerClass = SimplePPAPRequestHandler,
         ServerClass = ThreadingHTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
