# Author: Shadow Saint (Keerthan Bhat)
# This file contains the code for retrieving the data of places from .xlsx file and loading it into the SQLite database.
# Basically automation code in Python.

# importing openpyxl(third party module), and sqlite module
import openpyxl
import sqlite3

# get workbook and worksheet object
wb = openpyxl.load_workbook('places.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')

# get object for using the database
conn = sqlite3.connect('places.db')
c = conn.cursor()


# data in table 1: place
data = tuple(sheet['A6':'E114'])

for row in data:
    
    tup = []
    
    for cell in row:
        tup.append(cell.value)
    
    # converts list into tuple
    tup = tuple(tup)
    
    c.execute("INSERT INTO place VALUES ( ?, ?, ?, ?, ? )", tup)


# data in table 2: info
data = tuple(sheet['F6':'K114'])

i = 1
for row in data:
    
    tup = [i]
    i = i + 1
    
    for cell in row:
        tup.append(cell.value)
    
    tup = tuple(tup)
    
    c.execute("INSERT INTO info VALUES ( ?, ?, ?, ?, ?, ?, ? )", tup)


# data in table 3: extras
data = tuple(sheet['L6':'Q114'])

i = 1
for row in data:
    
    tup = [i]
    i = i + 1
    
    for cell in row:
        tup.append(cell.value)
    
    tup = tuple(tup)
    
    c.execute("INSERT INTO extras VALUES ( ?, ?, ?, ?, ?, ?, ? )", tup)
    

# commit changes in the database and close it
conn.commit()
conn.close()