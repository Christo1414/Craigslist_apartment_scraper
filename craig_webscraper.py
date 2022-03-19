"""Craiglist Webscraper version 1
This script defines the functions used to scrape apartment postings data from craigslist pages.
Search parameters hardcoded into URL to limit search to apartment and condo listings.
This script requires BeautifulSoup to parse and retrieve data from the returned HTML documents.

This script can be imported for use of the following functions:
    * scrape_craig(max_pages, time_sleep, print)
"""

import requests
import time
import re

from bs4 import BeautifulSoup

class Apartment:
    id = 0 
    date = ''
    ft2 = ''
    beds = ''
    price = '' 
    hood = ''
    link = ''
    
fields_apartment = ['id','date','ft2','beds','price','hood','link']


def craig_spider(max_pages, time_sleep):
    # use offset in URL to get next pages
    offset = 0
    max_offset = max_pages*120

    # set minimum time to sleep between get requests (seconds)
    min_sleep = 0.2
    if time_sleep < min_sleep:
        time_sleep = min_sleep 

    i_offset = 0
    apartments_total = []
    while offset < max_offset:
        
        if(offset != 0): #skip on first iteration, sleep briefly on subsquent iterations
            print("waiting "+ str(time_sleep) +"s before sending another GET request...")
            time.sleep(time_sleep)
        
        base = "https://vancouver.craigslist.org/search/apa?"
        append = "s=" + str(offset) + "&availabilityMode=0&housing_type=1&housing_type=2"
        url = base+append

        print("Sending GET request...")

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="search-results")

        listings = []
        apartments = []
        i=0
        #loop through results-row to store link in object for each posting
        for result in results.findAll('li',{"class": "result-row"}):
            apartments.append(Apartment())
            link = result.find("a")
            apartments[i].link = link['href']
            i+=1 

        #loop through results-info to analyze for additional information
        for list in results.findAll('div',{"class": "result-info"}):
            listings.append(list)
        
        i=0
        for listing in listings:
            droplisting = False
            apartments[i].date = listing.find('time',{'class':'result-date'}).text 
            apartments[i].price = listing.find('span',{'class':'result-price'}).text
            if(apartments[i].price == "$0"):
                droplisting = True
                
            #apartments[i].ft2 = listing.find('span',{'class':'housing'}).text
            for size in listing.findAll('span',{'class':'housing'}):
                apartments[i].ft2 = size.text
            apartments[i].hood = listing.find('span',{'class':'result-hood'}).text.strip()

            if(droplisting):
                apartments.pop(i)
                continue
            apartments[i].id = i + i_offset
            i+=1
            
        apartments_total.append(apartments)
        offset+=120
        i_offset += i
        
    return apartments_total


def print_apartments(apartments, i):
    err_count = 0
    page = i+1
    for apartment in apartments:
        try:
            print("Apartment #"+str(apartment.id + 1) + " on page " + str(page))
            print(apartment.date, apartment.price, apartment.ft2, apartment.hood)
            print(apartment.link)
        except:
            print("Error in apartment on page {index}".format(index = page))
            err_count+=1
        print("\n")

    print("Number of errors during print: " +str(err_count) +"\n")

def configure_size_value(apartments): 
    # iterates through list of Apartment objects to remove whitespace and set empty strings = 'n/a'
    for apartment in apartments:
        if(apartment.ft2 != ""):
            apartment.ft2 = re.sub(r"[\n\t\s]*", "",apartment.ft2)


#Import this function
def scrape_craig(max_pages, time_sleep, print):
    apartments_total = craig_spider(max_pages, time_sleep)
    for i in range(max_pages):
        configure_size_value(apartments_total[i])

        if(print):
            print_apartments(apartments_total[i], i)

    return apartments_total



# _______MAIN________
# scrape 1 page and print out postings

if __name__ == '__main__':
    apartments_total = scrape_craig(1,1,True)


