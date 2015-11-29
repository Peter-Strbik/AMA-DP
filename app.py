from flask import Flask, render_template, request
from utils import get_secret_key
import google, urllib2, bs4, re, requests
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        results = google.search(query, num = 10, start = 0, stop = 10)
        urls = []
        for i in results:
            urls.append(i)
        page = requests.get(urls[0])
        raw = page.text
        lessRaw = re.sub("<.*?>", "", raw)
        niceText = re.sub("[ \t\n]+", " ", lessRaw)
        return render_template('results.html', r=niceText)
    return render_template('index.html')

if __name__ == "__main__":
   app.debug = True
   app.secret_key = get_secret_key()
   app.run(host="0.0.0.0", port=8000)
