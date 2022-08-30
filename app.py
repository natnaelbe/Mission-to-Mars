from flask import Flask, render_template
from scraping import load_data_from_mongo
from scraping import scrape_all
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html', mars = {'hemispheres': load_data_from_mongo()})
@app.route('/scrape')
def scrape():
    scrape_all(True)
app.run(port=8000)