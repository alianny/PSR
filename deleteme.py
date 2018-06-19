import sqlite3
import sys

conn = sqlite3.connect('localPSR.db')
c = conn.cursor()

quote_list = ['06/18/2018', '33.02', '33.04', '32.1', '32.19', '78572530', '06/15/2018', '32.62', '33.27', '32.15', '33.15', '113679900', '06/14/2018', '32.6', '32.98', '32.1', '32.52', '88085310', '06/13/2018', '33', '33.14', '32.21', '32.22', '194948900', '06/12/2018', '34.51', '34.53', '34.08', '34.35', '55653180']

c.execute('CREATE TABLE IF NOT EXISTS t (date DATE PRIMARY KEY, Open FLOAT, Close FLOAT, High FLOAT, Low FLOAT, Volume FLOAT )')
print("----------------------")
print(len(c.fetchall()))
print("----------------------")




conn.commit()
conn.close()