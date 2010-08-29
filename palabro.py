import web
from datetime import date
from web.db import sqlwhere
from index import db

def get(palabro):
    result = db.select(
        'palabros', 
        what='*, UNIX_TIMESTAMP(publish) AS unix_publish', 
        where=sqlwhere({'palabro': palabro}))
    
    if result:
        word = result[0]
        
        word['date'] = date.fromtimestamp(word['unix_publish'])
        
        return word
    else:
        return False

def getLatest():
    result = db.select(
        'palabros', 
        what='*, UNIX_TIMESTAMP(publish) AS unix_publish', 
        where='publish <= DATE(NOW())', 
        order='publish DESC', 
        limit=1
    )
    
    if result:
        word = result[0]
        
        word['date'] = date.fromtimestamp(word['unix_publish'])
        
        return word
    else:
        return False
        
def getQueue():
    return db.select('palabros', where='publish > DATE(NOW())', order='publish DESC')
    
def add(palabro, hint, description):
    new_publish = db.select('palabros', what='DATE_ADD(MAX(publish), INTERVAL 1 DAY) AS new_publish')[0]['new_publish']
    db.insert('palabros', palabro=palabro, hint=hint, description=description, publish=new_publish)

def edit(palabro, hint, description):
    db.update('palabros', hint=hint, description=description, where=sqlwhere({'palabro': palabro}))
