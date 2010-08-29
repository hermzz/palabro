import web
from index import db

def get(palabro):
    return db.select('palabros', where='palabro="%s"' % palabro)

def getLatest():
    return db.select('palabros', order='id DESC', limit=1)
