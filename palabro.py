#coding=utf-8

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

def getNavWords(date):
    first_word = False
    prev_word = False
    
    next_word = False
    latest_word = False
    
    # get previous word
    prev_result = db.select(
        'palabros', 
        what='*, UNIX_TIMESTAMP(publish) AS unix_publish', 
        where='publish < "'+date.isoformat()+'"', 
        order='publish DESC', 
        limit=1
    )
    	
    if prev_result:
        prev_word = prev_result[0]
        
        first_result = db.select('palabros', what='*, UNIX_TIMESTAMP(publish) AS unix_publish', order='publish ASC', limit=1)[0]
        if first_result['publish'] != prev_word['publish']:
            first_word = first_result
    
    next_result = db.select(
        'palabros', 
        what='*, UNIX_TIMESTAMP(publish) AS unix_publish', 
        where='publish > "'+date.isoformat()+'" AND publish <= DATE(NOW())', 
        order='publish ASC', 
        limit=1
    )
    
    if next_result:
        next_word = next_result[0]
        
        latest_result = db.select('palabros', what='*, UNIX_TIMESTAMP(publish) AS unix_publish', where='publish <= DATE(NOW())', order='publish DESC', limit=1)[0]
        if latest_result['publish'] != next_word['publish']:
            latest_word = latest_result
    
    return {
        'first': first_word,
        'prev': prev_word,
        'next': next_word,
        'latest': latest_word
    }

def getRandom():
    return db.select('palabros', where='publish <= NOW()', order='RAND()', limit=1)[0]
    
def getRange(start, end):
    return db.select(
        'palabros', 
        where='publish >= "%s" AND publish <= "%s"' % (start, end), 
        order='publish DESC'
    )

def getArchive():
    return db.select(
        'palabros',
        what='publish, YEAR(publish) as year, MONTH(publish) AS month',
        where='DATE(publish) <= DATE(NOW())',
        group='year, month',
        order='publish DESC'
    )

def getMonthArchive(year, month):
    return db.select(
        'palabros',
        where=sqlwhere({'YEAR(publish)': year, 'MONTH(publish)': month}) + ' AND DATE(publish) <= DATE(NOW())',
        order='publish DESC'
    )
        
def getQueue():
    return db.select('palabros', where='publish > DATE(NOW())', order='publish DESC')
    
def add(palabro, hint, description):
    new_publish = db.select('palabros', what='DATE_ADD(MAX(publish), INTERVAL 1 DAY) AS new_publish')[0]['new_publish']
    db.insert('palabros', palabro=palabro, hint=hint, description=description, publish=new_publish)

def edit(palabro, hint, description):
    db.update('palabros', hint=hint, description=description, where=sqlwhere({'palabro': palabro}))
