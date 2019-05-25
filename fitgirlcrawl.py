# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:17:10 2019

@author: Raghav Utpat
"""

import requests
import bs4
import sqlite3

website = "https://www.fitgirl-repacks.site/all-my-repacks-a-z/"
pages = 22
insert = """INSERT INTO gamedata VALUES 
        ("{name}", "{tags}", "{company}", "{lang}", "{size1}", "{size2}");"""
connection = sqlite3.connect("D:/Games/allfitgirlgames.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE gamedata""")

cursor.execute( """CREATE TABLE gamedata (
    Name text,
    Genres_Tags text,
    Companies text,
    Languages text,
    Original_size real,
    Repack_size real);""")

def extractnum(data):
    splitter = ''
    num = []
    if '/' in data:
        splitter = '/'
    elif '~' in data:
        splitter = '~'
    else:
        splitter = ' '
    data = data.replace(',','.')
    data = data.split()
    data = [x.split(splitter) for x in data]
    for li in data:
        for word in li:
            try:
                num.append(float(word))
            except ValueError:
                pass
    print(num)
    return min(num)


for page in range(1,pages+1):
    resp = requests.get(website+"?lcp_page0="+str(page)+"#lcp_instance_0")
    soup = bs4.BeautifulSoup(resp.content,features = "lxml")
    catlist = soup.find_all("ul",class_="lcp_catlist")
    print(type(catlist))
    print(len(catlist))
    for link in catlist[0]:
        link = link.a.attrs['href']
        info = requests.get(link.replace('http','https'))
        soup1 = bs4.BeautifulSoup(info.content,features = "lxml")
        gamedata = soup1.body.p
        gamedata = bs4.BeautifulSoup(str(soup1.body.p).replace('<br />','<br />\n').replace('<br/>','<br />\n'))
        #gamedata = bs4.BeautifulSoup(str(soup1.body.p).replace('<br/>','<br />\n'))
        gamedata = gamedata.text.split('\n')
        print(gamedata)
        row = [soup1.head.title.text,None,None,None,None,None]
        for data in gamedata:
            if data is not '':
                if "Genre" in str(data.split(':')[0]):
                    row[1] = data.split(':')[1]
                elif('Compan' in data.split(':')[0]):
                    row[2] = data.split(':')[1]
                elif('Lang' in data.split(':')[0]):
                    row[3] = data.split(':')[1]
                elif('size' in data.split(':')[0]) or ('Size' in data.split(':')[0]):
                    if('MB' in data):
                        if('Original' in data):
                            row[4] = extractnum(data)/1024
                        elif('Repack' in data):
                            row[5] = extractnum(data)/1024
                    else:
                        if('Original' in data):
                            row[4] = extractnum(data)
                        elif('Repack' in data):
                            row[5] = extractnum(data)
                #else:
                 #   raise Exception(data)
        print(row)
        #raise Exception(row)
        cursor.execute(insert.format(name = row[0],tags = row[1],
                                     company = row[2],lang = row[3],
                                     size1 = row[4],size2 = row[5]))


            
connection.commit()
connection.close()