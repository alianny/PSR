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
    args = sys.argv[1:]
    if not args:
        print "No URL: Usage: %s querystring" % sys.argv[0]
        #RETURN SOMETHING
        return
    
    print "Launching Chrome Browser..."
    # specify the url
    WebBrowser = webdriver.Chrome()
    WebBrowser.get(sys.argv[1])

    print "Updating Website..."
    WebBrowser.find_element_by_xpath("""//*[@id="ddlTimeFrame"]/option[1]""").click()
    print "Waiting on Update..."
    time.sleep(2)
    #WebBrowser.find_element_by_xpath(sys.argv[2]).click()
    
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
