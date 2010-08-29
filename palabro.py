import web
from web.db import sqlwhere
from index import db

def get(palabro):
    return db.select('palabros', where=sqlwhere({'palabro': palabro})

def getLatest():
    return db.select('palabros', where='publish <= DATE(NOW())', order='id DESC', limit=1)
