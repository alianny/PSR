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

#Application will call python is the .csv dile does not exist or if the time requested is not up to date
def main():
    print "Evaluating Arguments..."
    # 1:Site #2: TimeFrame #3: Symbol
    if len(sys.argv) < 4: 
        print "Argument Number Problem: Usage: %s querystring" % sys.argv[0]
        time.sleep(5.5)
        #RETURN SOMETHING
        return
    
    time.sleep(2.5)
    print "Launching Chrome Browser..."
    # Use Chrome
    WebBrowser = webdriver.Chrome()
    # Go to Link provided
    print "Going to NASDAQ..."
    WebBrowser.get(sys.argv[1])

    #Update if other website ever needed
    quote_list = nasdaq(sys.argv[2], WebBrowser )
    for m in quote_list:
        print m
    time.sleep(2.5)
    print 
    if(WebBrowser):
        WebBrowser.close()


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
