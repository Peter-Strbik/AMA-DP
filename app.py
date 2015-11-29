from flask import Flask, render_template, request
from utils import get_secret_key, getTextFromSearch
import google, urllib2, bs4, re, requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        text = getTextFromSearch(query)
        return render_template('results.html', r=text)
    return render_template('index.html')

if __name__ == "__main__":
   app.debug = True
   app.secret_key = get_secret_key()
   app.run(host="0.0.0.0", port=8000)
