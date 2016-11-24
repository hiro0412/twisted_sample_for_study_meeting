# coding: utf-8

from urllib2 import urlopen
import sys
import re

server = "http://localhost:8000"

def fetch_item(path):
    url = '/'.join([server, str(path)])
    print url
    try:
        content = urlopen(url).read()
    except Exception as e:
        print >>sys.stderr, e
        return None
    else:
        return content


def main():

    def get_ppap(index):
        content = fetch_item(index)
        if not content:
            return None

        m = re.match('^.* (\w+)$', content)
        if not m:
            print >>sys.stderr, "invalid response:", content
            raise

        key = m.group(1)

        content = fetch_item(key)
        if not content:
            return None

        return '%s: %s = %s' % (index, key,content)


    for i in range(10):
        print get_ppap(i)

if __name__ == '__main__':
    main()
