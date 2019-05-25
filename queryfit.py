# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:32:12 2019

@author: Raghav Utpat

A demonstration on how to use the database created by fitgirlcrawl.py
"""

import sqlite3

columns = ['Name','Genres_Tags','Companies','Languages','Original_size','Repack_size']
query = """SELECT * from gamedata where {name} {and1} {genre} {and2} {size}"""
values = {"name" : "", "genre" : "", "size" : "", "and1" : "", "and2" : ""}
file = "D:/Games/allfitgirlgames.db"
connection = sqlite3.connect(file)
cursor = connection.cursor()

print("You can search by name , genre and repack size\nJust enter -1 to leave the field empty")
name = input("\nEnter name or part of name of the game : ")
genre = input("\nEnter genre or part of genre of the game : ")
size = input("\nEnter the max repack size in GB : ")
    
if(name == "-1" and genre == "-1" and size == "-1"):
    raise Exception("All fields are empty")
if(name != "-1"):
    values["name"] = columns[0]+" LIKE \'%"+name+"%\'"
if(genre != "-1"):
    values["genre"] = columns[1]+" LIKE \'%"+genre+"%\'"
if(size != "-1"):
    values["size"] = columns[5]+" < "+str(float(size))
if(name != "-1" and genre != "-1"):
    values["and1"] = "AND"
if(genre != "-1" and size != "-1"):
    values["and2"] = "AND"
if(name != "-1" and genre == "-1" and size != "-1"):
    values["and2"] = "AND"
        
query = query.format(name=values["name"], and1=values["and1"],
                     genre=values["genre"], and2=values["and2"],
                     size=values["size"])

cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    print(row)
    print("\n")

connection.close()
