from flask import Flask, request, jsonify
import requests
import time
import smtplib
from lxml.html import fromstring

app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to I hate soldout !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)