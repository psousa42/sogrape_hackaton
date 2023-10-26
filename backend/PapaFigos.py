import os
from time import sleep
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup
import datetime
import re
import time
import sys

uri = "mongodb+srv://opc:L5xJt6oXMKrCRiBv@cluster0.0xb5fg2.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

db = client["sogrape"]
collection = db["PapaFigos"]

link = "https://www.continente.pt/produto/papa-figos-doc-douro-vinho-branco-papa-figos-6274693.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36','Cookie':'Cookie: dwanonymous_921d4ae6710e4b2198d48293cc3ce075=abKOuLtMAhx7QCcaMZD0RafmS9; realUserVerifier=Verified; __cq_uuid=abKOuLtMAhx7QCcaMZD0RafmS9; __gads=ID=88b452bf7d22e0e6:T=1697709058:RT=1698167319:S=ALNI_MbpRl19M9X-dQ7cI5rSMjj6-JonCA; __gpi=UID=00000cbb924def5b:T=1697709058:RT=1698167319:S=ALNI_MZPsr6N27qV7jpj_t4pUtRalJdC-Q; __cq_seg=0~-0.52!1~-0.20!2~-0.46!3~-0.15!4~0.27!5~-0.27!6~0.04!7~-0.12!8~-0.51!9~-0.18!f0~3~1!n0~4; __cq_bc=%7B%22bdvs-continente%22%3A%5B%7B%22id%22%3A%222050174%22%7D%2C%7B%22id%22%3A%225427547%22%7D%2C%7B%22id%22%3A%222103486%22%7D%2C%7B%22id%22%3A%225400380%22%7D%2C%7B%22id%22%3A%227855352%22%7D%2C%7B%22id%22%3A%222922551%22%7D%2C%7B%22id%22%3A%223777012%22%7D%2C%7B%22id%22%3A%224342301%22%7D%2C%7B%22id%22%3A%227536694%22%7D%2C%7B%22id%22%3A%226078857%22%7D%5D%7D; dwac_99f34b6e35d78e56f04854e02c=dk9LyYQwX-IxyO8p-J26sULUf5i327vAY4w%3D|dw-only|||EUR|false|Europe%2FLisbon|true; cqcid=abKOuLtMAhx7QCcaMZD0RafmS9; cquid=||; sid=dk9LyYQwX-IxyO8p-J26sULUf5i327vAY4w; __cq_dnt=0; dw_dnt=0; dwsid=OJVnYVVOkJ7BVzaaszHZ5gwOUzBmpXS8kxNffW4uA1dBLzOKJmYg49V-5EVn5mbQ338JKo0ZDk0mI0vNaTmpJA==; GCLB=CKWC8dKK1-foTQ'}
response = requests.get(link, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

url = 'Continente'

product_name_element = soup.find(class_='pwc-h3 col-h3 product-name pwc-font--primary-extrabold mb-0')
product_name = f'{product_name_element.text.strip()}'

pattern = r'\b\d{4}\b'
matches = re.findall(pattern, product_name)

# Capacity
capacity_element = soup.find(class_='ct-pdp--unit col-pdp--unit')
product_type = capacity_element.text.strip()
capacity = product_type.split()[-2] + ' ' + product_type.split()[-1]
capacity = re.sub(r'[^0-9]', '', capacity)

price_elements = soup.find_all(class_='ct-price-formatted')
liter_element = soup.find(class_='ct-price-value')

value_element = soup.find(class_="ct-product-tile-badge-value--pvpr col-product-tile-badge-value--pvpr")
if not value_element:
	value_element = soup.find(class_="ct-product-tile-badge-value--pvpr col-product-tile-badge-value--pvpr col-product-tile-plusdesign")
	
elements_with_mb_0_class = soup.find_all(class_="mb-0")
target_text = "Origem:"
country_target_element = None

for element in elements_with_mb_0_class:
	if target_text in element.get_text(strip=True):
		country_target_element = element
		break

elements_with_mb_0_class = soup.find_all(class_="mb-0")
target_text = "Região:"
region_target_element = None

for element in elements_with_mb_0_class:
	if target_text in element.get_text(strip=True):
		region_target_element = element
		break

for price_element in price_elements:
	raw_price = price_element.text
	raw_liter = liter_element.text
	cleaned_price = raw_price.replace('(', '').replace(')', '').replace('€','').replace(',','.').strip()
	cleaned_liter = raw_liter.replace('(', '').replace(')', '').replace('€','').strip()
	formatted_price = f'{cleaned_price}€ por unidade'
	formatted_liter = f'{cleaned_liter}€ por litro'

	print(f'Store Name: {url}')
	print(f'Wine Name: {product_name}')
	if matches:
		harvest_year = matches[0]
		print("Harvest year:", harvest_year)
	else:
		harvest_year = "N\A"
		print('Harvest Year:', harvest_year)
	print(f'Capacity: {capacity}')
	print(f'Price: {formatted_price} || {formatted_liter}')
	if value_element:
		discount_value = value_element.text.strip()
		print(f"Discount: {discount_value}%")
	else:
		discount_value = "0"
		print("Discount: " + discount_value + "%")
	currency = "EUR" #change if needed
	print(f'Currency: {currency}')
	current_datetime = datetime.datetime.now()
	formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
	formatted_date = current_datetime.strftime("%Y-%m-%d")
	print("Current Date:", formatted_date)
	print("Current Date and Time:", formatted_datetime)
	if country_target_element:
			next_element = country_target_element.find_next(class_="mb-20")
			if next_element:
				country = next_element.get_text(strip=True)
			else:
				country = None
	else:
		country = None
	
	if region_target_element:
		next_element = region_target_element.find_next(class_="mb-20")
		if next_element:
			region = next_element.get_text(strip=True)
			#print(f"Location: {next_element.get_text(strip=True)}")
		else:
			region = None
	else:
		region = None

	if country and region:
		location = f"{country}, {region}"
	elif country:
		location = country
	elif region:
		location = region
	else:
		location = "N\A"

print(f'Location: {location}')
product_data = {
		"Store_name": url,
		"Product_name": product_name,
		"Harvest_year": harvest_year,
		"Capacity": product_type,
		"Price_unit": float(cleaned_price), 
		"Price_liter": cleaned_liter,
		"Discount": discount_value,
		"Currency": currency,
		"Date": formatted_date,
		"Location": location,
		"Country": country,
		"Region": region
	}
collection.insert_one(product_data)


###GARRAFEIRA SOARES###
link = "https://www.garrafeirasoares.pt/pt/portugal/vinhos/vinho-branco-douro-papa-figos-75-cl/item_10769.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(link, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

url = 'Garrafeira Soares'

product_name_element = soup.find(class_='name clearfix')
product_name = f'{product_name_element.text.strip()}'

pattern = r'\b\d{4}\b'
matches = re.findall(pattern, product_name)

product_type_element = soup.find(class_='col-sm-8 column column-info')
product_type = product_type_element.text.strip()

price_element = soup.find('div', class_='price').find('span', class_='current')
price_element = price_element.text.strip()

cleaned_price = price_element.replace('(', '').replace(')', '').replace('€','').replace(',','.').strip()
cleaned_liter = None

discount_tag = soup.find(class_='discount')

capacity = soup.find_all(class_='col-sm-8 column column-info')
for result in soup.find_all('div', class_='col-sm-8 column column-info'):
	capacity = result.find('p').get_text()
	if 'L' in capacity or 'cl' in capacity:
		break
capacity = re.sub(r'[^0-9]', '', capacity)
referencia = soup.find(class_='ref')
referencia = referencia.text.strip()

entrega = soup.find(class_='item-available')
entrega = entrega.text.strip()

shipment = soup.find(class_='time-delivery')
shipment = shipment.text.strip()

country_tag = soup.find('p', class_='title', string='País')
if country_tag:
	country = country_tag.find_next('p').get_text(strip=True)
else:
	country = None

region_tag = soup.find('p', class_='title', string='Região')
if region_tag:
	region = region_tag.find_next('p').get_text(strip=True)
else:
	region = None

if country and region:
	location = f"{country}, {region}"
elif country:
	location = country
elif region:
	location = region
else:
	location = "N\A"

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
formatted_date = current_datetime.strftime("%Y-%m-%d")

print("\n\n")
print(f'Store Name: {url}')
print(f'Wine Name: {product_name}')
if matches:
	harvest_year = matches[0]
	#print(f'Harvest Year: {matches[0]}')
	print (harvest_year)
else:
	harvest_year = "N\A"
	print('Harvest Year: N\A')
#print(f'Capacity: {capacity}')
print(f'Price: {price_element}')

if discount_tag and discount_tag.text.strip():
	discount_value = discount_tag.text.strip('%').split("-")[-1]
	print(f'Discount: {discount_value}%')
else:
	discount_value = "N\A"
	print("Discount: N\A")
currency = "EUR"
print('Currency: EUR €')
print(f'Current Date and Time: {formatted_datetime}')	
print(f'Location: {location}')

product_data = {
	"Store_name": url,
	"Product_name": product_name,
	"Harvest_year": harvest_year,
	#"capacity": capacity, #capacity in different unit scale (cl | L)
	"Price_unit": float(cleaned_price),
	"Price_liter": cleaned_liter, #missing unless we calculate it
	"Discount": discount_value,
	"Currency": currency,
	"Date": formatted_date,
	"Location": location,
	"Availability": entrega,
	"Shipment": shipment
}
collection.insert_one(product_data)
# print(f'Desconto: {discount}, {promo}')	
#print(f'Disponibilidade: {entrega}, {shipment}')
# print(f'{referencia}')

###ELCORTEINGLES###
link = "https://www.elcorteingles.pt/supermercado/0105218705602987-papa-figos-vinho-branco-do-douro-garrafa-75-cl/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(link, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
url = 'El Corte Ingles'
# Extract product title
title_element = soup.find('div', class_='page_title-text_container js-page-title-layer').find('h1')
product_name = title_element.text.strip() if title_element else 'N/A'

# Extract discounts
discount_element = soup.find('div', class_= 'prices-price _before')
full_price = discount_element.text.strip() if discount_element else 'N/A'
cleaned_price = full_price.replace('(', '').replace(')', '').replace('€','').strip()
price_search = 'prices-price _offer'
if not discount_element:
	price_search = 'prices-price _current'

# Extract price
price_element = soup.find('div', class_= price_search)
price = price_element.text.strip() if price_element else 'N/A'
cleaned_price = price.replace('(', '').replace(')', '').replace('€','').replace(',','.').strip()

#get discount value
current_price = cleaned_price.replace(',','.')
if discount_element:
	discount_value = int(100 - (float(current_price) * 100 / float(full_price.replace(',','.').replace('€',''))))
else:
	discount_value = 0;

# Extract product price per liter
price_per_liter_element = soup.find('div', class_='prices-price _pum')
price_per_liter = price_per_liter_element.text.strip() if price_per_liter_element else 'N/A'
cleaned_liter = price_per_liter.replace('(', '').replace(')', '').replace('€','').replace(' ','').replace('/','€/').strip()

# Extract reference
reference_element = soup.find('div', class_='reference-container pdp-reference').find('span', class_='hidden')
reference = reference_element.text.strip() if reference_element else 'N/A'

# Extract year
year_element = soup.find('div', class_= 'pdp-title mb').find('p')
year_name = f'{year_element.text.strip()}'
pattern = r'\b\d{4}\b'
matches = re.findall(pattern, year_name)

# Extract capacity
capacity = year_name.split()[-2] + ' ' + year_name.split()[-1]
capacity = re.sub(r'[^0-9]', '', capacity)
# Scrapping date
current_datetime = datetime.datetime.now()
formatted_date = current_datetime.strftime("%Y-%m-%d")

#currency
currency = "EUR"

#location
location = "N/A"
print("\n\n")
print(f'Site: {url}')
print(f'Nome: {product_name}')
if matches:
	harvest_year = matches[0]
	print(f'Harvest Year: {matches[0]}')
else:
	harvest_year = "N/A"
	print('Harvest Year: N\A')
print(f'Capacity: {capacity}')
print(f'Price: {cleaned_price}€ || {cleaned_liter}')
print(f'Discount: {discount_value}%')
print('Currency: EUR €')
print(f'Current Date and Time: {formatted_date}')	
print(f'Location: N\A')
print(f'EAN: {reference}\n')

product_data = {
	"Store_name": url,
	"Product_name": product_name,
	"Harvest_year": harvest_year,
	"Capacity": capacity,
	"Price_unit": float(cleaned_price),
	"Price_liter": cleaned_liter,
	"Discount": discount_value,
	"Currency": currency,
	"Date": formatted_date,
	"Location": location
}
collection.insert_one(product_data)