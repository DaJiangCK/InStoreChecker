from lxml import html
import requests
from time import sleep
import time
import schedule
import smtplib
import os
# from decouple import config

receiver_email_id = "mayanjun0110@gmail.com"

def check(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    # adding headers to show that you are
    # a browser who is sending GET request
    page = requests.get(url, headers=headers)
    for _ in range(20):
        # because continuous checks in
        # milliseconds or few seconds
        # blocks your request
        sleep(3)
        # parsing the html content
        doc = html.fromstring(page.content)
        # checking availaility
        # XPATH_AVAILABILITY = '//div[@id ="purchase-attributes-size-notification-error"]//text()'
        XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
        AVAILABILITY = ''.join(
            RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        return AVAILABILITY


def sendemail(url):
    GMAIL_USERNAME = os.environ['G_USERNAME']
    GMAIL_PASSWORD = os.environ['G_PASSWD']
    # GMAIL_USERNAME = config('G_USERNAME')
    # GMAIL_PASSWORD = config('G_PASSWD')

    print(GMAIL_USERNAME)
    print(GMAIL_PASSWORD)
    recipient = receiver_email_id
    body_of_email = url
    email_subject = 'Lululemo product availability'

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    # message to be sent
    headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                           "subject: " + email_subject,
                           "to: " + recipient,
                           "mime-version: 1.0",
                           "content-type: text/html"])

    content = headers + "\r\n\r\n" + body_of_email
    s.sendmail(GMAIL_USERNAME, recipient, content)
    s.quit()


def readUrlsFromFile():
    url_file = open('urls.txt', 'r') 
    item_urls = url_file.readlines()
    url_file.close()
    # arr = "Sold out online."
    arr = [ 
        'Only 1 left in stock.', 
        'Only 2 left in stock.', 
        'In stock.'] 
    for url in item_urls:
        url = url.strip()
        print("Processing: "+url)
        ans = check(url)
        print(ans)
        if ans in arr:
            # sending email to user if
            # in case product available
            sendemail(url)

# scheduling same code to run multiple
# times after every 1 minute
def job():
    print("Tracking....")
    readUrlsFromFile()


schedule.every(6).hours.do(job)

while True:

    # running all pending tasks/jobs
    schedule.run_pending()
    time.sleep(1)
