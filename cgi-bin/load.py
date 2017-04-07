#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi,os
import sqlite3
import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
from myutils import check_file,CAT

exist_tor=check_file('./DB/torrents.db3')
exist_con=check_file('./DB/content.db3')

print('content­type: text/html\n')
print('''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Обновление базы</title>
<link rel="stylesheet" type="text/css" href="../infotor.css" />
</head><body>
<script language="JavaScript" type="text/javascript">
  function showBlock(t) {
    var elStyle = document.getElementById( t ).style;
        elStyle.display = (elStyle.display == 'none') ? '' : 'none';}
  function do_all(source) {
  for(i=0;i<24;i++)  {
	document.getElementById('razd'+(i+1)).checked=source.checked;}}
  function do_one(source) {
	if(!source.checked)	{
	document.getElementById('main').checked=false;}
	else {set_checked=true;
	    for(i=0;i<24;i++) {
		if(!document.getElementById('razd'+(i+1)).checked) {
		    set_checked=false;
		break;}}
		if(set_checked)	{
		document.getElementById('main').checked=true;}}}
function tcount() {
    showBlock('wt');
    var start=0;
    document.getElementById("watch").innerHTML = '00:00:00';
        setInterval(function(){
            start++;
            var seconds = Math.floor( (start/1) % 60 );
  			var minutes = Math.floor( (start/1/60) % 60 );
  			var hours = Math.floor( (start/(1*60*60)) % 24 );
  			seconds = (seconds < 10) ? "0"+seconds : seconds;
			minutes = (minutes < 10) ? "0"+minutes : minutes;
			hours = (hours < 10) ? "0"+hours : hours;
			counter_time=hours+':'+minutes+':'+seconds;

            document.getElementById("watch").innerHTML = counter_time;
        }, 1000);}
function validator(){
	if (document.optload.backup.value=="")
		{alert('Нет файла бэкапа, с которого будет проводится загрузка!');
		document.optload.backup.focus();
		return false}
	else {tcount();	return true};}
</script>
<div class="layer1"><h1>Обновление базы InfoTor</h1></div>
<div class="layer3">
<table style="width: 100%; position:relative">
<tr><td style="width:20%">&nbsp;</td><td style="vertical-align:middle;"><div class="fs1" name="Group1">
<form class="opt" method="post" action="load1.py" name="optload" onsubmit="return validator(this)" style="left: 0px; top: 45px; height: 376px">
<table style="border: 2px #C0C0C0 solid; width:100%; margin:0px 10px 0px 10px">
<tr class="tr80"><td style="width:10%; text-align:center;"><p>1.</p></td>''')

http_1='''<td><p{}>Создать основной файл БД torrents.db3 если его нет*</p></td>
<td style="text-align:center"><p>
<input name="opt1" type="checkbox" {} value="tor" {} /></p></td></tr>'''

if exist_tor==True:
    print(http_1.format(' style="color: #C0C0C0"','','disabled="disabled"'))
else:
    print(http_1.format('','checked="checked"',''))

http_2='''<tr class="tr80"><td style="width:10%; text-align:center;"><p>2.</p></td>
<td><p{}>Создать файл БД content.db3 описаний раздач если его нет</p></td>
<td style="text-align:center;"><p><input name="opt2" type="checkbox" {} {} value="con" /></p></td></tr>'''    

if exist_con==True:
    print(http_2.format(' style="color: #C0C0C0"','','disabled="disabled"'))
else:
    print(http_2.format('','checked="checked"',''))

print('''<tr class="tr80"><td style="width:10%; text-align:center;"><p>3.</p></td>
<td><p>Файл <b>backup.*.xml</b></p></td>
<td><p align="right"><span title="Выберите файл обновления. Если в этом поле пусто, то поместите в каталог INFOTOR/UPDATE файл и обновите страницу">
<select name="backup" value="" style="width: 200px">''')

if check_file('./UPDATE/backup.*.xml')==True:
    for f in sorted(os.listdir('./UPDATE'),reverse=True):
        if f[:8] == 'backup.2':
            print('<option value="{}">{}</option>\n'.format(f,f))
    
print('''</select></span></p></td></tr>
<tr class="tr80"><td style="width:10%; text-align:center;"><p>4.</p></td><td><p>Загружаемые категории:</p></td><td>&nbsp;</td></tr>
<tr class="tr80"><td>&nbsp;</td>
<td colspan="2"><div class="sp-wrap" style="left:10%"><div class="sp-head folded"><a href="#" onclick="showBlock('bl1'); return false"><span class="sp-w">Список</span></a></div>
<div class="sp-body" id="bl1" style="display: none;">
<table cellpadding="0" cellspacing="0 "class="auto-style2" style="width: 100%">''')
print('''<tr><td></td><td></td><td style="border-bottom:1px solid #C0C0C0; text-align:center"><p><input type="checkbox" checked="checked" id="main" onclick="do_all(this);" /></p></td></tr>''')
http_3='''<tr><td style="width:10%; text-align:center;"><p>{}</p></td><td style="width:70%; text-align:left;"><p>{}</p></td>
    <td style="text-align:center;"><p><input name="razd" type="checkbox" id="razd{}" {} value="{}" onclick="do_one(this);" /></p></td></tr>'''
num=0
if exist_tor==False:
    for key in sorted(CAT.keys()):
        if key!='00':
            num+=1
            print(http_3.format(key,CAT[key],num,'checked="checked"',key))
else:
    DB=sqlite3.connect('DB/torrents.db3')
    cur=DB.cursor()
    cur.execute('SELECT code_category,name_category,load_category FROM category ORDER BY code_category')
    r=cur.fetchall()
    for rr in r:
        num+=1
        razdel=('0'+str(rr[0]))[-2:]
        if rr[2]==1:
            print(http_3.format(razdel,rr[1],num,'checked="checked"',razdel))
        else:
            print(http_3.format(razdel,rr[1],num,'',razdel))
    cur.close()
    DB.close()

print('''</table></div></div></td></tr>
<tr class="tr80"><td style="width:10%; text-align:center;"><p>5.</p></td>
<td><p>Выполнить сжатие базы после загрузки обновления</p></td>
<td style="text-align:center"><p><input name="vac" type="checkbox" checked="checked"/></p></td></tr>
<tr><td colspan="3" style="text-align:right; vertical-align: middle; padding-bottom: 20px; padding-top: 10px;">
<hr><p><input name="Submit1" type="submit" value="Выполнить" /></p><hr></td>
</tr>
<tr><td colspan="3"><p style="margin:0px 20px 20px 50px; font-size:8pt; color:grey;">* - При загрузке обновления из
очередного бэкапа существующая информация из баз удаляется и на ее место записывается новая</p></td></tr>
</table></form></div>
</td><td style="width:20%">&nbsp;</td>
</tr></table><br />

</div>
<div class="layer4" >
<table class="subtable" cellpadding="0" cellspacing="0">
<tr><td width="30%"></td>
<td width="40%" style="text-align:center"><p>- 2017 -</p></td>
<td align="right"><p>&copy; Y3401</p></td>
</tr></table></div>
<div class="home"><a class="cl1" href="../index.html" title="На главную страницу"></a></div>
<div class="back"><a class="cl1" href="javascript:history.back()" title="Назад"></a></div>
<div class="wait" id="wt" style="display:none"><div class="wait-content"><table style="width:100%; height:100%;">
<tr><td style="width:100%; height:100%; vertical-align:middle"><p><span id="watch">000</span></p>
</td></tr></table>
<div id="comment">Загрузка и обработка файла может занять продолжительное время. До 2.5-3 часов. <br />
Не закрывайте это окно, дождитесь завершения!</div>
</div></div>
</body></html>''')

