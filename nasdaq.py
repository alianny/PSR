import sys
import re
from selenium import webdriver
import time
from lxml import html
import sqlite3
# import libraries


#csv libs
import csv
from datetime import datetime

print( "Python Program Running...")

#Application will call python is the .csv dile does not exist or if the time requested is not up to date
def main():
    print( "Evaluating Arguments...")
    # 1:Site #2: TimeFrame #3: Symbol #4 database
    if len(sys.argv) < 3: 
        print( "Argument Number Problem: Usage: %s querystring" % sys.argv[0])
        time.sleep(5.5)
        #RETURN SOMETHING
        return
    
    time.sleep(2.5)
    print( "Launching Chrome Browser...")
    # Use Chrome
    WebBrowser = webdriver.Chrome()
    # Go to Link provided
    print( "Going to NASDAQ...")
    WebBrowser.get(sys.argv[1])

    #Update if other website ever needed
    quote_list = nasdaq(sys.argv[2], WebBrowser )

    #Assume, that if we are here the local database is there
    print("Connnecting to database...")
    conn = sqlite3.connect('localPSR.db')
    c = conn.cursor()

    #Determine whether we need to create a database or just update it
    print( "Creating database...")
    c.execute( '''CREATE TABLE IF NOT EXISTS ''' + sys.argv[3] + ''' (date DATE PRIMARY KEY, Open FLOAT, Close FLOAT, High FLOAT, Low FLOAT, Volume FLOAT )''' )
    print( "Closing database...")

    #submit to the database and delete from list
    print(type(quote_list))

    while len(quote_list) > 0:
        print(quote_list[:6])
        templist = [tuple(quote_list[:6])]
        print (templist)
        c.executemany('''INSERT OR IGNORE INTO ''' + sys.argv[3] + ''' VALUES (?,?,?,?,?,?)''', templist)
        del quote_list[:6]


    conn.commit()
    conn.close()


    time.sleep(2.5)
 
    if(WebBrowser):
        WebBrowser.close()


def nasdaq( sysArugments, Web ):

    originalSource = Web.page_source

    print( "Updating Website...")
    putQuotes = '''%s'''% sysArugments
    find_option_number = re.findall(r'\d+', sysArugments)
    waitTime = .5 * float(find_option_number[0])
    #//*[@id="ddlTimeFrame"]/option[1]
    Web.find_element_by_xpath(putQuotes).click()

    print( "Waiting on %s ms for website update..." % waitTime)
    time.sleep(waitTime)
    
    print( "Extracting Table...-***NEEDS WORKS***")
    
    tree = html.fromstring(Web.page_source)
    table = tree.xpath("""//*[@id="quotes_content_left_pnlAJAX"]/table/tbody//text()""", smart_strings=False)

    table = [number.replace('\n','') for number in table]
    table = [number.replace("'",'') for number in table]
    table = [number.replace(",",'') for number in table]
    table = [number.replace(" ",'') for number in table]
    table = ' '.join(table).split()

    #delete first 5 entries, they are garbage
    del table[:6]

    #str_list = filter(None, table)
    return table

if __name__ == '__main__':
    main()
