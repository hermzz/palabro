import web, os, sys

web.config.debug = False

path = os.path.dirname(__file__)
if path:
    os.chdir(path)
    sys.path.insert(0,path)

import palabro

urls = (
    '/(.*)', 'word'
)

db = web.database(dbn='mysql', user='root', pw='', db='palabro')
web.template.Template.globals['frender'] = web.template.frender
render = web.template.render('templates', base='main')

class word:
    def GET(self, word):
        if word != 'index.py/':
            result = palabro.get(word)
        else:
            result = palabro.getLatest()
        
        if result:
            return render.word({'word': result[0]})
            

app = web.application(urls, globals())

def internalerror():
    return web.internalerror("Bad, bad server. No donut for you.")

def notfound():
    return web.notfound("Whatever you're lookin' for it ain't here")

app.internalerror = internalerror
app.notfound = notfound

application = app.wsgifunc()

