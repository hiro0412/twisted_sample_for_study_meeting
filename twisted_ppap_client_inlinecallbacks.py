# coding: utf-8

from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer
import sys
import traceback
import re

server = "http://localhost:8000"


def fetch_item(path):
    url = '/'.join([server, str(path)])
    print url
    d = getPage(url)
    return d


def main():

    @defer.inlineCallbacks
    def get_ppap(index):
        try:
            content = yield fetch_item(index)
        except Exception as e:
            print >>sys.stderr, e
            raise
            
        m = re.match('^.* (\w+)$', content)
        
        if not m:
            print >>sys.stderr, "invalid response:", content
            raise

        key = m.group(1)

        try:
            content = yield fetch_item(key)
        except Exception as e:
            print >>sys.stderr, e
            raise

        defer.returnValue('%s: %s = %s' % (index, key,content))


    def callback(content):
        print content
        return content
        
    ds = []
    for i in range(10):
        d = get_ppap(i)
        d.addCallbacks(callback)
        ds.append(d)

    def callbackForDList(res):
        print "== result =="
        for r in res:
            print r

        reactor.stop()

    dlist = defer.DeferredList(ds, consumeErrors=True)
    dlist.addCallback(callbackForDList)

    reactor.run()


if __name__ == '__main__':
    main()
