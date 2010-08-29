import web, os, sys, locale, markdown

web.config.debug = False

path = os.path.dirname(__file__)
if path:
    os.chdir(path)
    sys.path.insert(0,path)

import palabro
from config import config

urls = (
    '/backend/?', 'listQueue',
    '/backend/edit/(.*)', 'editWord',
    '/backend/add', 'addWord',
    '/(.*)', 'word'
)

locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

db = web.database(**config['db'])
web.template.Template.globals['markdown'] = markdown.markdown
render = web.template.render('templates', cache=False, base='main')

class word:
    def GET(self, word):
        if word != 'index.py/':
            result = palabro.get(word)
        else:
            result = palabro.getLatest()
        
        if result:
            return render.word({'word': result})

class listQueue:
    def GET(self):
        words = palabro.getQueue()
        return render.listQueue(words)

class editWord:
    def GET(self, word):
        result = palabro.get(word);
        
        if result:
            return render.editWord(result)

    def POST(self, word):
        palabro.edit(word, web.input()['hint'], web.input()['description'])
        web.seeother('/backend/edit/%s' % word)
        
class addWord:
    def GET(self):
        return render.addWord()
    
    def POST(self):
        palabro.add(web.input()['palabro'], web.input()['hint'], web.input()['description'])
        web.seeother('/backend/')
               

app = web.application(urls, globals())

def internalerror():
    return web.internalerror("Bad, bad server. No donut for you.")

def notfound():
    return web.notfound("Whatever you're lookin' for it ain't here")

app.internalerror = internalerror
app.notfound = notfound

application = app.wsgifunc()

