#coding=utf-8

import web, os, sys, locale, markdown
import datetime
from datetime import date, timedelta
from PyRSS2Gen import RSS2, RSSItem, Guid
from urllib import urlencode

web.config.debug = False

# this tells web.py to _not_ append index.py/ to redirects
os.environ["REAL_SCRIPT_NAME"] = ''

path = os.path.dirname(__file__)
if path:
    os.chdir(path)
    sys.path.insert(0,path)

import palabro
from config import config

urls = (
    # backend
    '/backend/?', 'listQueue',
    '/backend/edit/(.*)', 'editWord',
    '/backend/add', 'addWord',
    
    # extras
    '/acerca-de', 'sobre',
    '/archivo/([0-9]+)/([0-9]+)', 'archiveMonth',
    '/archivo', 'archive',
    '/aleatorio', 'aleatorio',
    '/rss', 'rss',
    
    # default
    '/(.*)', 'word'
)

locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

db = web.database(**config['db'])
web.template.Template.globals['markdown'] = markdown.markdown
web.template.Template.globals['config'] = config
web.template.Template.globals['urlencode'] = urlencode
render = web.template.render('templates', cache=False, base='main')

class word:
    def GET(self, word):
        if word != 'index.py/':
            result = palabro.get(word)
        else:
            result = palabro.getLatest()
        
        if result:
            # get first, previous, next and latest words
            return render.word({'word': result, 'nav_words': palabro.getNavWords(result['date'])})
        else:
            raise web.notfound(render.wordnotfound())

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

class sobre:
    def GET(self):
        return render.sobre()

class archive:
    def GET(self):
        years = palabro.getArchive()
        return render.archive(years)
        
class archiveMonth:
    def GET(self, year, month):
        words = palabro.getMonthArchive(year, month)
        return render.archiveMonth(date(int(year), int(month), 1), words)

class aleatorio:
    def GET(self):
        word = palabro.getRandom()
        web.seeother('/%s' % word.palabro, True)

class rss:
    def GET(self):
        start_date = date.today() + timedelta(days=-90)
        end_date = date.today()
        words = palabro.getRange(start_date.isoformat(), end_date.isoformat())
        
        rss_words = []
        for word in words:
            rss_words.append(
                RSSItem(
                    title = u"Palabra del día: %s" % word.palabro,
                    link = u"http://palabro.es/%s" % word.palabro,
                    description = markdown.markdown(word.description),
                    guid = Guid(u"http://palabro.es/%s" % word.palabro),
                    pubDate = datetime.datetime(word.publish.year, word.publish.month, word.publish.day, 0, 0, 0)
                )
            )
        
        rss = RSS2(
            title = u"palabro.es",
            link = "http://palabro.es",
            description = u"Feed RSS de palabro.es",
            lastBuildDate = datetime.datetime.now(),
            items = rss_words
        )
        
        web.header('Content-type', "application/rss+xml; charset=utf-8")
        return rss.to_xml(encoding='utf-8')

app = web.application(urls, globals())

def internalerror():
    return web.internalerror(render.internalerror())

def notfound():
    return web.notfound(render.notfound())

app.internalerror = internalerror
app.notfound = notfound

application = app.wsgifunc()

