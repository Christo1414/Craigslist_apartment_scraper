'''  analyze_strings.py
Parses and formats the different strings of scraped data.
Specifically,
    -reformatting apartment.ft2 to extract #bedrooms and remove letters/symbols
        if #br- not present assume 1br
        if ft2 not present assume average value
    -parsing apartment.hood and categorizing into one of 6 cities
        ["north van","new west","burnaby","richmond","vancouver","surrey"]
    -parse apartment.price and remove the following symbols: "$, 

This script can be imported for use of the following functions:
    * reformat_strings(apartment)               - does the above formatting
    * generate_list_strings(apartments_total)   - transforms each object into a list of strings
'''




from craig_webscraper import Apartment

def init_apartment():
    Apartment.id = 0
    Apartment.date = 'Feb 14'
    Apartment.ft2 = '1br-n/a'
    Apartment.price = '"$3,800"'
    Apartment.hood = '( city of vancouver )'
    Apartment.link = 'https://vancouver.craigslist.org/van/apa/d/vancouver-park-west-unfurnished/7438951919.html'



def generate_list_strings(apartments_total):
    records = []
    for apartments in apartments_total:
        for apartment in apartments:
            row = [str(apartment.id), apartment.date, apartment.ft2, apartment.beds, apartment.price, apartment.hood, apartment.link]
            records.append(row)
    return records


def reformat_strings(apartment):

    # remove symbols from price
    apartment.price = apartment.price.strip('"').lstrip("$").replace(',','')

    # parse hood and categorize into city
    apartment.hood = apartment.hood.lstrip('(').rstrip(')').lower()
    fullstring = apartment.hood
    cities = ["north van","new west","burnaby","richmond","downtown","vancouver","surrey","coquitlam"]
    check2 = True
    for city in cities:
        if city in fullstring:
            apartment.hood = city
            check2 = False
            break
    if check2:
        if "tricities" in fullstring:
            apartment.hood = "coquitlam"
            
        elif "north shore" in fullstring or "n van" in fullstring:
            apartment.hood = "north van"
        elif "yaletown" in fullstring or "coal harbour" in fullstring:
            apartment.hood = "downtown"
        

    #change apartment size into sqft/bedroom
    fullstring = apartment.ft2
    if fullstring.find("ft2") != -1:
        if fullstring.find("br") != -1:
            split_index = fullstring.find("br")
            beds = fullstring[0:split_index]
            ft2 = fullstring[split_index+3:fullstring.find("ft2")]
        else:
            beds = 1
            ft2 = fullstring[0:fullstring.find("ft2")]
    elif fullstring.find("br") != -1:
        ft2 = 'n/a' # set to average later
        beds = fullstring[0:fullstring.find("br")]
    else:
        ft2 = 'n/a'
        beds = 'n/a'

    apartment.beds = beds
    apartment.ft2 = ft2

    return apartment


# _______MAIN________
# initialize a sing object with some test data. Format and print

if __name__ == '__main__':
    init_apartment()
    apartment = Apartment()
    apartment_reformatted = reformat_strings(apartment)

    print(apartment_reformatted.price)
    print(apartment_reformatted.hood)
    print(apartment_reformatted.beds, apartment_reformatted.ft2)