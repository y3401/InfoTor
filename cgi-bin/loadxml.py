#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# модуль парсинга дампа БД "RuTracker.org" и загрузки в БД sqlite InfoTor

import xml.sax
#import os, os.path
import sys
import sqlite3, zlib

k = 0
num1=0
num2=0

class TorHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.tid = ''
        self.reg_date = ''
        self.b_size = ''
        self.title = ''
        self.url = ''
        self.magnet = ''
        self.forum_id = ''
        self.forum = ''
        self.contents = ''

   # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        global tid, reg_date, b_size, forum_id
        if tag == 'torrent':
            tid = attributes['id']
            reg_date = attributes['registred_at']
            b_size = attributes['size']
        elif tag == 'forum':
            forum_id = attributes['id']
            
                   
   # Call when an elements ends 
    def endElement(self, tag):
        global magnet, forum, title, k, contents, num1
        if self.CurrentData == 'url':
            pass
        elif self.CurrentData == 'magnet':
            magnet = self.magnet
            magnet = magnet.replace('magnet:?xt=urn:btih:','')
            magnet = magnet.replace('&tr=1','')
            self.magnet = ''
        elif self.CurrentData == 'forum':
            forum = self.forum
            forum=forum.replace('"',"'")
            self.forum = ''
        elif tag == 'content':
            contents = self.contents
            self.contents = ''
        elif tag == 'title':
            title = self.title
            self.title = ''
        elif tag == 'torrent':
            k += 1
            num1 += 1
            category = check_forum(forum_id,forum)
            for rzd in razdel:
                if int(category)==int(rzd):
                    write_tor(category,forum_id,tid,magnet,title,b_size,reg_date)
                    if f_c==True:
                        write_content(tid,contents)
            if k == 1000:
                DB.commit()
                if f_c==True:
                    DB1.commit()
                k = 0
        self.CurrentData = ''
        
   # Call when a character is read
    def characters(self, content):
        if self.CurrentData == 'title':
            self.title += content
        elif self.CurrentData == 'url':
            self.url = content
        elif self.CurrentData == 'magnet':
            self.magnet += content
        elif self.CurrentData == 'forum':
            self.forum += content
        elif self.CurrentData == 'content':
            self.contents += content

def check_forum(kod_podr,name_podr): # проверка наличия форума в базе, добавление или апдейт
    c=DB.cursor()
    c.execute('SELECT * FROM podr WHERE podr_number=?', (kod_podr,))
    row=c.fetchall()
    if len(row) == 0:
        c.execute('INSERT INTO podr(podr_number,podr_name,kod_cat) VALUES (?,?,0)', (kod_podr,name_podr))
    else:
        c.execute('UPDATE podr SET podr_name=? WHERE podr_number=?', (name_podr, kod_podr))
    c.execute('SELECT kod_cat FROM podr WHERE podr_number=?',(kod_podr,))
    result=c.fetchone()
    c.close()
    return result[0]

def write_tor(id_razd,id_podr,id_file,hash_info,title,size_b,date_reg):
    global num2,num3
    DB.execute('INSERT INTO torrent(razd_id,podr_id,file_id,hash_info,title,size_b,date_reg) VALUES (?,?,?,?,?,?,?);', (id_razd,id_podr,id_file,hash_info,title,size_b,date_reg))
    num2 += 1
            
def write_content(id_tor, cont):
    C = zlib.compress(cont.encode())
    DB1.execute('INSERT INTO cont(id_tor,content) SELECT ?,?', (id_tor, C))

def load_xml(backup, file_tor, file_con=''):
    global DB,DB1,f_c,razdel
    f_c=False
    razdel=[]
    DB=sqlite3.connect(file_tor)
    if file_con!='':
        DB1=sqlite3.connect(file_con)
        f_c=True
    cur=DB.cursor()
    cur.execute('SELECT kod_cat FROM razd WHERE load_cat=1')
    r=cur.fetchall()
    for rr in r:
        razdel.append(rr[0])
        
    parser = xml.sax.make_parser()                              # create an XMLReader
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)    # turn off namepsaces
    Handler = TorHandler()                                      # override the default ContextHandler
    parser.setContentHandler( Handler )

    parser.parse(backup)
    DB.commit()
    DB.close()
    if f_c==True:
        DB1.commit()
        DB1.close()
    return ((num1,num2))


