import requests
import time
import smtplib
from lxml.html import fromstring
import os
item_urls = ['https://shop.lululemon.com/p/sale/Define-Jacket-MD/_/prod8240254?color=37121&sz=6', 'https://shop.lululemon.com/p/sale/Back-In-Action-Ls-MD/_/prod8970067?color=27574&sz=4']
to_email = 'mayanjun0110@gmail.com'
key_word = "Sold out online"

while len(item_urls):
    print(item_urls)
    page = requests.get(item_urls[0])
    print(page.url)
    pages = [requests.get(item_url) for item_url in item_urls]
    for page in pages:
        tree = fromstring(page.content)
        item_name = tree.findtext('.//title')
        if key_word not in page.text:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('mayanjun0110@gmail.com', 'yan1jun10')
            message = 'Subject: Your item {} is in store\n\n{}'.format(item_name, page.url)
            s.sendmail("sender_email_id", to_email, message)
            s.quit()
            item_urls.remove(page.url)
            print('Item {} is in store!'.format(item_name))
        else:
            print('Item {} is sold out'.format(item_name))
    time.sleep(60)
