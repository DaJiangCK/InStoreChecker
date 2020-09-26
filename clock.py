import requests
import time
import smtplib
from lxml.html import fromstring
from flask import Flask, request, jsonify
import os
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    item_urls = ['https://shop.lululemon.com/p/sale/Define-Jacket-MD/_/prod8240254?color=37121&sz=6', 'https://shop.lululemon.com/p/sale/Back-In-Action-Ls-MD/_/prod8970067?color=27574&sz=4']
    to_email = 'mayanjun0110@gmail.com'
    key_word = "Sold out online"

    pages = [requests.get(item_url) for item_url in item_urls]
    for page in pages:
        tree = fromstring(page.content)
        item_name = tree.findtext('.//title')
        if key_word not in page.text:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(os.environ['G_USERNAME'], os.environ['G_PASSWD'])
            message = 'Subject: Your item {} is in store\n\n{}'.format(item_name, page.url)
            s.sendmail("sender_email_id", to_email, message)
            s.quit()
            item_urls.remove(page.url)
            print('Item {} is in store!'.format(item_name))
        else:
            print('Item {} is sold out'.format(item_name))

sched.start()
