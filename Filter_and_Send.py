'''Filter_and_Send.py

Use this script to filter the apartment data csv file and send an email
containing the postings that meet the requirements of price and location.


'''
import os
import smtplib
import pandas as pd
from matplotlib import pyplot as plt
from email.message import EmailMessage

EMAIL_ADD = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASS = os.environ.get('EMAIL_PASSWORD')
RECEIVER = os.environ.get('RECEIVER')

def send_email(filename):
    # Reads a CSV file and sends the data in the message body

    message = EmailMessage()
    message['Subject'] = "TEST SUBJECT"
    message['From'] = EMAIL_ADD
    message['To'] = RECEIVER

    with open(filename, 'r') as f:
        file = f.read()
    f.close()

    message.set_content(file)

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()         
        smtp.starttls()     
        smtp.ehlo()         

        smtp.login(EMAIL_ADD, EMAIL_PASS)


        smtp.send_message(message)
    
    print("Email Sent!")


def check_params(price_thresh,location):
    #verify filtering parameters are correct

    locations = ["vancouver", "downtown", "north van", "burnaby", "richmond"]
    try: 
        locations.index(location)
    except:
        print("Location not recognized, deaulting to 'downtown'...")
        location = "downtown"

    if price_thresh < 0 or price_thresh >20000:
        print("Price outside of range[0, 20000], defaulting to 2000...")
        price_thresh = 2000

    return price_thresh,location


def filter_listings(filename, price_thresh,location):
    # this will read a csv file and create a new one containing listings
    # under threshold price and in a certain location.
    # default to under 2000$ in downtown. 

    outfile = 'apartments_email.csv'

    price_thresh, location = check_params(price_thresh,location)
    
    data = pd.read_csv(filename)
    data_ut = data[data.price <= price_thresh]
    data_location = data_ut[data_ut.hood == location]
    data_location.to_csv(outfile,index=False,header=False)
    return outfile


def filter_and_send(filename,price_thresh = 2000,location = "downtown"):
    outfile = filter_listings(filename,price_thresh,location)
    send_email(outfile)


# _______MAIN________
# test functionality with incorrect parameters

if __name__ == '__main__':
    filter_and_send('test_feb15_1.csv')