import sys
import re
from selenium import webdriver
import time
from lxml import html
# import libraries
from bs4 import BeautifulSoup

#csv libs
import csv
from datetime import datetime

print "Python Program Running..."

def main():
    print "Evaluating Arguments..."

    if len(sys.argv) < 3:
        print "Argument Number Problem: Usage: %s querystring" % sys.argv[0]
        #RETURN SOMETHING
        return
    

    print "Launching Chrome Browser..."
    # specify the url
    WebBrowser = webdriver.Chrome()

    WebBrowser.get(sys.argv[1])

    print "Going to NASDAQ..."
    #Update if other website ever needed
    quote_list = nasdaq(sys.argv[2], WebBrowser )
    for m in quote_list:
        print m
    
    print "Creating CSV FILE..."
    # query the website and return the html to the variable 'page'
    #page = urllib2.urlopen(sys.argv[1])

    # parse the html using beautiful soup and store in variable `soup`
    #soup = BeautifulSoup(table, 'html.parser')

    if(WebBrowser):
        WebBrowser.close()
    # get the index price
    #price_box = soup.find_all("tbody")
    #price = price_box.text
    #print price_box

    # open a csv file with append, so old data will not be erased
    with open('index.csv', 'a') as csv_file:
       writer = csv.writer(csv_file)
       writer.writerow([quote_list])

def nasdaq( sysArugments, Web ):

    originalSource = Web.page_source

    print "Updating Website..."
    putQuotes = '''%s'''% sysArugments
    find_option_number = re.findall(r'\d+', sysArugments)
    waitTime = .5 * float(find_option_number[0])
    #//*[@id="ddlTimeFrame"]/option[1]
    Web.find_element_by_xpath(putQuotes).click()

    print "Waiting on %s ms for website update..." % waitTime
    time.sleep(waitTime)
    
    print "Extracting Table...-***NEEDS WORKS***"
    
    tree = html.fromstring(Web.page_source)
    table = tree.xpath("""//*[@id="quotes_content_left_pnlAJAX"]/table/tbody//text()""", smart_strings=False)

    table = [number.replace('\n','') for number in table]
    table = [number.replace("'",'') for number in table]
    table = [number.replace(",",'') for number in table]
    table = [number.replace(" ",'') for number in table]
    str_list = filter(None, table)
    return str_list

if __name__ == '__main__':
    main()
