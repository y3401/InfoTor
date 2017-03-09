#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi,os
import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import myutils as mU
from loadxml import load_xml
import time

form = cgi.FieldStorage()
file_tor=''     # флаг создания основной базы
file_con=''     # флаг создания файл контента
backup=''       # имя загружаемого файла
category=[]     # загружаемые категории
vac=''          # флаг сжатия базы после обновления
n=0             # номер строки в ответе
rep_back=()     # возвращаемое значение всего и загружено
time_begin = 0  # начало процесса
time_end = 0    # конец процесса

time_begin=time.time()

if "opt1" in form.keys(): file_tor=form.getfirst("opt1")
if "opt2" in form.keys(): file_con=form.getfirst("opt2")
if "razd" in form.keys(): category=form.getlist("razd")
if "backup" in form.keys(): backup=form.getfirst("backup")
if "vac" in form.keys(): vac=form.getfirst("vac")



print('content­type: text/html\n')
print('''<!DOCTYPE html>
<html><head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Обновление базы</title>
<link rel="stylesheet" type="text/css" href="../infotor.css" />
</head><body><div class="layer1"><h1>Обновление завершено</h1></div>
<div class="layer3">
    <div class="report" style="width: 400px; margin: 0 auto; display: block; position: relative">
    <table style="width: 100%; display: block;">
	<tr><td style="padding: 30px; vertical-align:middle; padding-top: 10px;">''')

if file_tor=='tor':
    mU.load_category()
    mU.create_db()
    mU.load_forums()
    mU.ins_forums(mU.List)
    n+=1
    print('<p>%s. Основная база torrents.db3 создана</p>' % n)
    n+=1
    print('<p>%s. Справочники категорий и форумов заполнены</p>' % n)
    
if file_con=='con':
    mU.create_db_content()
    n+=1
    print('<p>%s. База описаний контента content.db3 создана</p>' % n)

    # очистить таблицы
if mU.check_file('DB/torrents.db3')==True:
    mU.clear_torrents()
if mU.check_file('DB/content.db3')==True:
    mU.clear_content()
n+=1
print('<p>%s. Выполнена полная очистка таблиц</p>' % n)

n+=1
print('<p>%s. Загружаются следующие категории:</p><ul style="margin-left:40px; background-color:#F0F0F0">' % n)

for ctgr in mU.CAT.keys():
    if ctgr in category:
        print('<li><p>%s</p></li>' % mU.CAT[ctgr])
        mU.up_cat(ctgr,1)
    else:
        mU.up_cat(ctgr,0)
print('</ul>')

period = backup.split(".")[1][:8]
n+=1
print('<p>{}. Загружается обновление от <b>{}.{}.{}</b></p><br />'.format(n,period[-2:],period[4:6],period[:4]))
mU.up_period(period)

if mU.check_file('DB/content.db3')==True:
    rep_back=load_xml('UPDATE/'+backup,'DB/torrents.db3','DB/content.db3')
else:
    rep_back=load_xml('UPDATE/'+backup,'DB/torrents.db3')

n+=1
print('<p>{}. Обработано: <b>{}</b> записей.</p>'.format(n, rep_back[0]))
n+=1
print('<p>{}. Записано: &nbsp;&nbsp;&nbsp;<b>{}</b> записей</p>'.format(n, rep_back[1]))
if vac=='on':
    if mU.check_file('DB/torrents.db3')==True:
        mU.vacu('DB/torrents.db3')
    if mU.check_file('DB/content.db3')==True:
        mU.vacu('DB/content.db3')
    n+=1
    print('<p>%s. Выполнено сжатие баз</p>' % n)

time_end=time.time()
tsec=time_end-time_begin
stsec=(str(tsec)).split('.')
tsec=int(stsec[0])
seconds=0
minutes=0
hours=0
seconds=tsec % 60
minutes=(tsec//60) % 60
hours=(tsec//3600) % 24

n+=1
print('<p>{}. Общее затраченное время - <b>{}:{}:{}</b></p>'.format(n, str(hours),('0'+str(minutes))[-2:],('0'+str(seconds))[-2:]))

print('<p style="color:brown">Обновление выполнено. Теперь для экономии места на диске можно удалить файл <b>"backup.*.xml"</b> из каталога <b>/UPDATE</b> </p>')
print('''<p style="text-align:right"><input type="button" value="Готово" onclick="window.open('main.py','_parent');" name="ready" style="width: 95px" />''')
print('''</p></td></tr></table></div></div>
<div class="layer4" >
<table class="subtable" cellpadding="0" cellspacing="0">
<tr><td width="30%"></td>
<td width="40%" style="text-align:center"><p>- 2017 -</p></td>
<td align="right"><p>&copy; Y3401</p></td>
</tr></table></div>
<div class="home"><a class="cl1" href="../index.html" title="На главную страницу"></a></div>
</body></html>''')
