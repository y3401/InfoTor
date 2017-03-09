#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import sqlite3

List=[]
CTG=[]
D = {}

def check_file(file_name='*',status=False):
    if glob.glob(file_name): status=True
    return status

CAT={'00':'...','01':'Обсуждения, встречи, общение', '02':'Кино, Видео и ТВ', '04':'Новости',
     '08':'Музыка', '09':'Программы и дизайн', '10':'Обучающее видео', '11':'Разное',
     '18':'Сериалы', '19':'Игры', '20':'Документалистика и юмор', '22':'Рок-музыка',
     '23':'Электронная музыка', '24':'Все по авто и мото', '25':'Книги и журналы',
     '26':'Apple', '27':'Медицина и здоровье', '28':'Спорт', '29':'Мобильные устройства',
     '31':'Джазовая и Блюзовая музыка', '33':'Аудиокниги', '34':'Обучение иностранным языкам',
     '35':'Популярная музыка', '36':'ОБХОД БЛОКИРОВОК','37':'Hi-Res форматы, оцифровки'}

def load_forums():
    # Загрузка словаря форумов из файла CSV
    for line in open('DB/forums.csv', encoding = 'utf-8'):
        forum = line.split(sep=';"')[0]
        category = line.split(sep='";')[1]
        name_forum=line.split(sep=';"')[1].split(sep='";')[0]
        List.append((int(forum),name_forum,int(category)))

def load_category():
    # Загрузка словаря категорий из файла CSV
    for line in open('DB/category_info.csv', encoding = 'utf-8'):
        kod_cat = line.split(sep=';')[0].replace('"','')
        name_category=line.split(sep=';')[1].replace('"','')
        D[kod_cat] = name_category
        CTG.append((int(kod_cat),name_category))

def create_db():    #Создание базы и заполнение таблицы категорий

    DB=sqlite3.connect('DB/torrents.db3')
    cur=DB.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS "category"
    ("code_category" smallint NOT NULL PRIMARY KEY,
    "name_category" varchar(50) NOT NULL,
    "load_category" bool NOT NULL);

    CREATE TABLE IF NOT EXISTS "forum"
    ("code_forum" smallint NOT NULL PRIMARY KEY,
    "name_forum" varchar(80) NOT NULL,
    "category_id" smallint NOT NULL REFERENCES "category" ("code_category"));

    CREATE INDEX IF NOT EXISTS "forum_category_id_48a15a32" ON "forum" ("category_id");

    CREATE TABLE IF NOT EXISTS "torrent"
    ("file_id" integer NOT NULL PRIMARY KEY,
    "hash_info" varchar(40) NOT NULL,
    "title" varchar(255) NOT NULL,
    "size_b" integer NOT NULL,
    "date_reg" varchar(20) NOT NULL,
    "forum_id" smallint NOT NULL REFERENCES "forum" ("code_forum"));

    CREATE INDEX IF NOT EXISTS "torrent_forum_id_b67937c0" ON "torrent" ("forum_id");

    CREATE TABLE IF NOT EXISTS "vers"
    ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "vers" varchar(8) NOT NULL);

    INSERT INTO vers(vers) VALUES ('00000000');
    """)
    cur.executescript('DELETE FROM category; DELETE FROM forum; DELETE FROM torrent;')
    cur.executemany('INSERT INTO category(code_category,name_category,load_category) VALUES (?, ?, 1);', CTG)
    DB.commit()
    cur.close()
    DB.close()

def create_db_content(): # Создание доп. БД для хранения описаний раздач
    DB=sqlite3.connect('DB/content.db3')
    cur=DB.cursor()
    cur.executescript("""
    CREATE TABLE "contents"
    ("tid" integer NOT NULL PRIMARY KEY,
    "cont" text NOT NULL);

    DELETE FROM contents;
    """)
    cur.close()
    DB.close()

def get_vers():
    DB=sqlite3.connect('DB/torrents.db3')
    cur=DB.cursor()
    cur.execute('SELECT vers FROM vers') #получить дату версии БД
    vers=cur.fetchone()[0]
    cur.close()
    DB.close()
    return vers

def ins_forums(lists):
    DB=sqlite3.connect('DB/torrents.db3')
    for LLL in lists:
        try:
            DB.execute('INSERT INTO forum(code_forum,name_forum,category_id) VALUES (?, ?, ?);', LLL)
        except:
            pass
    DB.commit()

def clear_content():
    DB=sqlite3.connect('DB/content.db3')
    DB.execute('DELETE FROM contents')
    DB.commit()
    DB.execute('vacuum')
    DB.close()

def clear_torrents():
    DB=sqlite3.connect('DB/torrents.db3')
    DB.execute('DELETE FROM torrent')
    DB.commit()
    DB.execute('UPDATE vers set vers="00000000"')
    DB.commit()
    DB.execute('vacuum')
    DB.close()

def up_cat(razd=0,key=1):
    if razd!=0:
        DB=sqlite3.connect('DB/torrents.db3')
        cur=DB.cursor()
        #if check_file('DB/contents.db3')==True:
        #    cur.execute('ATTACH "DB/content.db3" as con')
        #    cur.execute('DELETE FROM cont WHERE id_tor IN (SELECT file_id FROM torrent WHERE razd_id='+str(razd)+');')
        #cur.execute('DELETE FROM torrent WHERE razd_id=?;', (str(razd),))
        cur.execute('UPDATE category SET load_category=? WHERE code_category=?;', (key,str(razd)))
        DB.commit()
        DB.close()

def up_period(period):
    DB=sqlite3.connect('DB/torrents.db3')
    cur=DB.cursor()
    cur.execute('UPDATE vers set vers="{}"'.format(period))
    DB.commit()
    DB.close()
        
def vacu(file=''):
    if file!='':
        DB=sqlite3.connect(file)
        DB.execute('vacuum')
        DB.close()

