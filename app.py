import requests
import time
import smtplib
from lxml.html import fromstring
from flask import Flask, request, jsonify
import os
app = Flask(__name__)

item_urls = ['https://shop.lululemon.com/p/sale/Define-Jacket-MD/_/prod8240254?color=37121&sz=6', 'https://shop.lululemon.com/p/sale/Back-In-Action-Ls-MD/_/prod8970067?color=27574&sz=4']

def checkInvetory():
    to_email = 'mayanjun0110@gmail.com'
    key_word = "Sold out online"

    while len(item_urls):
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
        time.sleep(60)

@app.route('/getlist/', methods=['GET'])
def respond():
    response = {}
    response["MESSAGE"] = f"I'm monitoring {item_urls}!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    checkInvetory()
    return "<h1>Checking list is empty !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
