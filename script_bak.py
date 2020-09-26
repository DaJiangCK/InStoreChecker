# Python script for Amazon product availability checker 
# importing libraries 
from lxml import html 
import requests 
from time import sleep 
import time 
import schedule 
import smtplib  
  
# Email id for who want to check availability 
receiver_email_id = "mayanjun0110@gmail.com"
  
  
def check(url): 
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} 
      
    # adding headers to show that you are 
    # a browser who is sending GET request 
    page = requests.get(url, headers = headers)  
    for i in range(20): 
        # because continuous checks in  
        # milliseconds or few seconds 
        # blocks your request 
        sleep(3)  
          
        # parsing the html content 
        doc = html.fromstring(page.content) 
          
        # checking availaility 
        XPATH_AVAILABILITY = '//div[@id ="purchase-attributes-size-notification-error"]//text()'
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY) 
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        return AVAILABILITY 
  
      
def sendemail(url): 
    GMAIL_USERNAME = os.environ['G_USERNAME']
    GMAIL_PASSWORD = os.environ['G_PASSWD']
      
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
  
  
def ReadAsin(): 
    url = "https://shop.lululemon.com/p/sale/Define-Jacket-MD/_/prod8240254?color=37121&sz=6"
    print ("Processing: "+url) 
    ans = check(url) 
    arr = "Sold out online."
    print(ans)
    if ans != arr:
        # sending email to user if  
        # in case product available  
        sendemail(url)  
  
# scheduling same code to run multiple 
# times after every 1 minute  
def job(): 
    print("Tracking....")  
    ReadAsin() 
  
schedule.every(1).minutes.do(job) 
  
while True: 
      
    # running all pending tasks/jobs 
    schedule.run_pending()  
    time.sleep(1) 