#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import sqlite3
import re
import codecs
import zlib
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import modbbcode

def calc(bsize=0):
    it=0
    razmer=['б','Кб','Мб','Гб','Тб']
    while bsize>1024:
        bsize/=1024
        it+=1
    if it>0:
        p=str(bsize).split(".")
        return ('{} '+razmer[it]).format(round(bsize,2))
    else:
        return ('{} '+razmer[0]).format(int(bsize))

def sel_content(id_tor):
    DB=sqlite3.connect('./DB/content.db3')
    cur=DB.cursor()
    cur.execute('SELECT content FROM cont WHERE id_tor=?;', (id_tor,))
    r=cur.fetchone()
    if r:
        S=zlib.decompress(r[0])
        result = modbbcode.bbcode2html(S.decode('utf-8'))
    else:
        result = '''<h3 style="text-align:center">Запись отсутствует</h3>'''
    cur.close()
    DB.close()
    return result

form = cgi.FieldStorage()
tid=0

if "tid" in form.keys(): tid=int(form.getfirst("tid"))

DB=sqlite3.connect('./DB/torrents.db3')
cur=DB.cursor()
cur.execute('''SELECT name_cat, podr_name, hash_info, title, size_b, date_reg
    FROM (torrent AS t inner join podr AS p on t.podr_id=p.podr_number) inner join razd AS r on t.razd_id=r.kod_cat
    WHERE file_id=%s;''' % tid)
r=cur.fetchone()
cur.close()
DB.close()

html_head='''<!DOCTYPE HTML>
<html><head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>%s</title>
<link rel="stylesheet" type="text/css" href="../infotor.css" />
</head><body>
<script language="JavaScript" type="text/javascript">
    function showBlock(t) {
           var elStyle = document.getElementById( t ).style;
           elStyle.display = (elStyle.display == 'none') ? '' : 'none'}
</script>
<div class="layer6">
'''

print('content­type: text/html\n')
if r:
    print(html_head % (r[3]))
    print('''<table class="subtable"><tr>''')
    print('''<td style="vertical-align:top;"><p class="info">{}<br />&rArr; {}</p></td>'''.format(r[0],r[1]))
    print('''<td style="width: 18%; vertical-align:middle"><p class="info">Размер: <b>{}</b></p></td>'''.format(calc(r[4])))
    print('''<td style="width: 25%; vertical-align:middle" align="right"><p class="info"><b>{}</b> {}</p></td>'''.format(r[5][:10],r[5][11:]))
    print('''<td style="width: 7%;"><a href="magnet:?xt=urn:btih:{}"><img src="../IMG/download40.png" align="right" alt="Скачать" title="Скачать по magnet-ссылке"></a></td></tr></table></div>'''.format(r[2]))
    print('''<div class="layer3" style="position: fixed;  top: 50px; background-color: rgb(227,227,227);">''')
    print('''<div class="layer5"><h2>{}</h2></div>'''.format(r[3]))
else:
    print(html_head % '')
    print('''<div class="layer3" style="position: fixed;  top: 50px; background-color: rgb(227,227,227);">''')
print('''<div class="post_body">''')
print(sel_content(tid))
print('''<br /><br /></div></div>
<div class="layer4">
<table class="subtable" cellpadding="0" cellspacing="0">
<tr><td width="30%"><p>...</p></td>
<td width="60%" align="center"><p>...</p></td>
<td style="text-align:right"><p style="margin-top:5px">&copy;Y3401</p></td>
</tr></table></div>''')
print('''<div class="clo"><a class="cl1" href="javascript:window.close()" title="Закрыть"></a></div></body></html>''')
