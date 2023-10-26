from time import sleep
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup
import datetime
import re
import time
import json
import sys

import requests
from bs4 import BeautifulSoup
import json

link = input("give me the link to the product -->")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(link, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with type="application/ld+json"
json_elements = soup.find_all(type="application/ld+json")
if json_elements:
    print(json_elements)
    # Iterate through each JSON element and modify the data
    for element in json_elements:
        # Extract text content of the element
        json_string = element.text

        # Parse the JSON string into a dictionary
        data = json.loads(json_string)

        # Remove the "price" key from the dictionary
        if 'offers' in data and 'price' in data['offers']:
            print(data['name'])
            print(data['image'])
            print(data['offers']['price'])
            print(data['offers']['priceCurrency'])
        else:
            print("\n\n" + json_string)
        # Convert the modified dictionary back to a JSON string
        modified_json_string = json.dumps(data, indent=4)

    # Print the modified JSON string
    # print("\n\n" + modified_json_string)
else:
    offer_elements = soup.find_all(itemtype="http://schema.org/Offer")
    for offer_element in offer_elements:
        # Find the <meta> tags inside the <span> element
        price = offer_element.find("span",itemprop="price")
        meta_price = offer_element.find("meta", itemprop="price")
        meta_price_currency = offer_element.find("meta", itemprop="priceCurrency")
        

        if price:
            print(price)
        # Check if the <meta> tags are found, and print their content
        if meta_price and meta_price_currency:
            print(meta_price)
            print(meta_price_currency)
        else:
            print("Meta tags not found for price and price currency.")
