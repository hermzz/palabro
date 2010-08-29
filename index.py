import web, os, sys

web.config.debug = False

path = os.path.dirname(__file__)
if path:
    os.chdir(path)
    sys.path.insert(0,path)

import palabro

urls = (
    '/index.py/', 'main',
    '/(.*)', 'word'
)

db = web.database(dbn='mysql', user='root', pw='', db='palabro')

class main:
    def GET(self):
        result = palabro.getLatest()
        if result:
            word = result[0]
            return 'Word for %s: %s<br />%s' % (word.publish, word.palabro, word.description)

class word:
    def GET(self, word):
        result = palabro.get(word)
        if result:
            word = result[0]
            return 'Word for %s: %s<br />%s' % (word.publish, word.palabro, word.description)
            

app = web.application(urls, globals())

def internalerror():
    return web.internalerror("Bad, bad server. No donut for you.")

def notfound():
    return web.notfound("Whatever you're lookin' for it ain't here")

app.internalerror = internalerror
app.notfound = notfound

application = app.wsgifunc()

