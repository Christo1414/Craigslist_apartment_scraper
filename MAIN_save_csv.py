"""save_csv.py
Generates a csv file of apartment postings data from craigslist, or appends to existing file. 
This script requires craig_webscraper.py and analyze_strings.py to be in the working folder

Run as main to scrape three pages of craigslist apartment postings and save to csv
Will clean up data and remove duplicate entries
"""

import csv
import os
from pathlib import Path
from craig_webscraper import scrape_craig, fields_apartment
from analyze_strings import reformat_strings, generate_list_strings
from remove_duplicates import remove_duplicates


def reformat_all(apartments_total):
    print("Cleaning up strings...")

    for apartments in apartments_total:
        for apartment in apartments:
            apartment = reformat_strings(apartment)

    return apartments_total
    

def write_file(filename, records, write_headers):
    with open(filename,'a',encoding="utf-8") as file:
        write = csv.writer(file)
        if write_headers:
            write.writerow(fields_apartment)
        write.writerows(records)
    file.close()


def scrape_save(max_pages,filename):

    apartments_total = scrape_craig(max_pages,1,False)

    apartments_reformatted = reformat_all(apartments_total)

    records = generate_list_strings(apartments_reformatted)

    if Path(os.getcwd()+"\\"+filename).is_file():
        print("File exists! appending data...")
        write_file(filename,records,False)
    else:
        print("Generating new csv file...")
        write_file(filename,records,True)

    
        
# _______MAIN________
# scrape three pages and save to test.csv
# then get duplicate entries removed

if __name__ == '__main__':
    scrape_save(3,"test.csv")
    remove_duplicates("test.csv")