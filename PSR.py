import sys
from selenium import webdriver
import time
# import libraries
import urllib2
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
    originalSource = WebBrowser.page_source
    
    print "Updating Website..."
    putQuotes = '''%s'''% sys.argv[2]

    #WebBrowser.find_element_by_xpath("""//*[@id="ddlTimeFrame"]/option[1]""").click()
    WebBrowser.find_element_by_xpath(putQuotes).click()
    print "Waiting on Update..."
    while (originalSource == WebBrowser.page_source):
        print "Waiting half of second..."
        time.sleep(.5)

    #WebBrowser.find_element_by_xpath(sys.argv[2]).click()
    #WebBrowser.find_element_by_xpath(//*[@id="quotes_content_left_pnlAJAX"]/table/tbody)
    print "Creating CSV FILE..."
    # query the website and return the html to the variable 'page'
    #page = urllib2.urlopen(sys.argv[1])

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(WebBrowser.page_source, 'html.parser')

    WebBrowser.close()
    # get the index price
    price_box = soup.find_all("tbody")
    #price = price_box.text
    print price_box


    # open a csv file with append, so old data will not be erased
    with open('index.csv', 'a') as csv_file:
       writer = csv.writer(csv_file)
       writer.writerow([price_box, datetime.now()])


if __name__ == '__main__':
    main()
