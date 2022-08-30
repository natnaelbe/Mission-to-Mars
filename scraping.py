from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import pymongo
from pymongo import server_api
client = pymongo.MongoClient("mongodb+srv://natnael:EMYA0XfRz6MYaLTT@cluster0.imfiiot.mongodb.net/?retryWrites=true&w=majority")
from webdriver_manager.chrome import ChromeDriverManager
def scrape_all(f):
    data = mars_facts()
    mydb = client["mars"]
    mycol = mydb["scraped_data"]
    if f == True:
        for d in data:
            x = mycol.insert_one(d)
def mars_facts():
    # Import Splinter, BeautifulSoup, and Pandas
    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ### Visit the NASA Mars News Site

    # Visit the mars nasa news site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []

    initial_landing_page_html = browser.html

    mars_soup = soup(initial_landing_page_html, 'html.parser')

    all_item_divs = mars_soup.find_all('div', class_='item')

    for div in all_item_divs:
        
        url = div.findChild("a")
        url_str = url.get('href')
        print("https://astrogeology.usgs.gov"+url_str)
        
        
        browser.visit("https://astrogeology.usgs.gov"+url_str)
        image_html = browser.html
        image_soup = soup(image_html, 'html.parser')
        image_url = image_soup.find('a', text='Sample')
        image_title = image_soup.find('h2', class_='title')
        hemisphere_image_urls.append({'img_url': image_url['href'], 'title': image_title.text})
    browser.quit()
    return(hemisphere_image_urls)

#scrape_all(False)

def load_data_from_mongo():
    mydb = client["mars"]
    mycol = mydb["scraped_data"]

    data = mycol.find()
    ret_data = []
    for x in data:
        ret_data.append(x)
    return ret_data
