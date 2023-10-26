from time import sleep
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup
import datetime
import re
import time
import sys

link = input("give me the link to the product -->")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
		   'Cookie':'Cookie: dwanonymous_921d4ae6710e4b2198d48293cc3ce075=abKOuLtMAhx7QCcaMZD0RafmS9; realUserVerifier=Verified; __cq_uuid=abKOuLtMAhx7QCcaMZD0RafmS9; __gads=ID=88b452bf7d22e0e6:T=1697709058:RT=1698167319:S=ALNI_MbpRl19M9X-dQ7cI5rSMjj6-JonCA; __gpi=UID=00000cbb924def5b:T=1697709058:RT=1698167319:S=ALNI_MZPsr6N27qV7jpj_t4pUtRalJdC-Q; __cq_seg=0~-0.52!1~-0.20!2~-0.46!3~-0.15!4~0.27!5~-0.27!6~0.04!7~-0.12!8~-0.51!9~-0.18!f0~3~1!n0~4; __cq_bc=%7B%22bdvs-continente%22%3A%5B%7B%22id%22%3A%222050174%22%7D%2C%7B%22id%22%3A%225427547%22%7D%2C%7B%22id%22%3A%222103486%22%7D%2C%7B%22id%22%3A%225400380%22%7D%2C%7B%22id%22%3A%227855352%22%7D%2C%7B%22id%22%3A%222922551%22%7D%2C%7B%22id%22%3A%223777012%22%7D%2C%7B%22id%22%3A%224342301%22%7D%2C%7B%22id%22%3A%227536694%22%7D%2C%7B%22id%22%3A%226078857%22%7D%5D%7D; dwac_99f34b6e35d78e56f04854e02c=dk9LyYQwX-IxyO8p-J26sULUf5i327vAY4w%3D|dw-only|||EUR|false|Europe%2FLisbon|true; cqcid=abKOuLtMAhx7QCcaMZD0RafmS9; cquid=||; sid=dk9LyYQwX-IxyO8p-J26sULUf5i327vAY4w; __cq_dnt=0; dw_dnt=0; dwsid=OJVnYVVOkJ7BVzaaszHZ5gwOUzBmpXS8kxNffW4uA1dBLzOKJmYg49V-5EVn5mbQ338JKo0ZDk0mI0vNaTmpJA==; GCLB=CKWC8dKK1-foTQ',
		   'Alt-Svc':'clear',
		   'Cache-Control':'max-age=0',
		   'Sec-Ch-Ua':'"Chromium";v="116", "Not)A;Brand";v="24", "Opera GX";v="102"',
		   'Sec-Fetch-User':'?1'
		   }
response = requests.get(link, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')


test = soup.find_all("script", "application/ld+json")
print(test)