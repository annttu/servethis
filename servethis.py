#!/usr/bin/env python
# encoding: utf-8

import os
import sys
from bottle import static_file, route, run, abort, request

PREFIX = ''
PATHS = [os.getcwd()]

def static(filename):
    for path in PATHS:
        if os.path.isfile(os.path.join(path,filename)):
            res = static_file(filename, root=path)
            res.set_header("Cache-Control","no-cache")
            res.set_header('Access-Control-Allow-Origin', '*')
            return res
    abort(404, "File not found")

@route(PREFIX + '/', ["GET", "POST"])
def callback():
    print(request.body.readlines())
    return static('index.html')

@route(PREFIX + '/<filename:path>')
def callback(filename):
    return static(filename)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            if not os.path.isdir(p):
                print("Not such file or directory %s" % p)
                sys.exit(1)
        PATHS=sys.argv[1:]
    print("Serving %s" % PATHS)
    try:
        run(host='localhost', port=8010, debug=True, reloader=True)
    except KeyboardInterrupt:
        sys.exit(0)
