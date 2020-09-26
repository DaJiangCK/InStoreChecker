from flask import Flask, request, jsonify
import requests
import time
import smtplib
from lxml.html import fromstring

app = Flask(__name__)

@app.route('/getitem/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    url = request.args.get("url", None)
    size = request.args.get("sz", None)

    # For debugging
    print(f"got url {url}")
    print(f"got fize {size}")

    response = {}

    # Check if user sent a name at all
    if not url or not size:
        response["ERROR"] = "no url or size found, please send a name and size."
    # Now the user entered a valid name
    else:
        to_email = 'mayanjun0110@gmail.com'
        key_word = "Sold out online"
        page = requests.get(url+'&sz='+size)
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
            response["MESSAGE"] = f"Item {item_name} is in store!"
        else:
            response["MESSAGE"] = f"Item {item_name} is sold out!!"
        

    # Return the response in json format
    return jsonify(response)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to I hate soldout !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)