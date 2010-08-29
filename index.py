import web, os, sys

web.config.debug = False

path = os.path.dirname(__file__)
if path:
    os.chdir(path)
    sys.path.insert(0,path)

import palabro

urls = (
    '/.*', 'main',
    )

db = web.database(dbn='mysql', user='root', pw='', db='palabro')

class main:
    def GET(self):
        result = palabro.getLatest()
        if result:
            word = result[0]
            return '%s<br />%s' % (word.palabro, word.description)

application = web.application(urls, globals()).wsgifunc()

