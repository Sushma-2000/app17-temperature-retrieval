import datetime
import threading
import time
from time import strftime

import pandas as pd
import requests
import selectorlib

URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
def scrape(url):
    """Scrape the page source from URL"""
    response = requests.get(url,headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor= selectorlib.Extractor.from_yaml_file("extract.yaml")
    value= extractor.extract(source)["temperature"]
    return value

def read_content():
    with open("data.txt","r") as file:
        content = file.read()
    return content

def store(date_now,temperature):
    content = read_content()
    with open("data.txt","w") as file:
        content = content + "\n" + date_now+","+temperature
        file.write(content)
    print("temperature stored")

def put_data():
    print("storing data")
    scraped = scrape(URL)
    extracted_temperature = extract(scraped)
    date = datetime.datetime.now()
    formatted_date = date.strftime('%Y-%m-%d-%H-%M-%S')
    store(formatted_date, extracted_temperature)

def start_scraping():
    global scraping_thread, stop_scraping
    stop_scraping = False

    def run():
        while not stop_scraping:
            put_data()
            time.sleep(5)  # scrape every 5 seconds

    scraping_thread = threading.Thread(target=run)
    scraping_thread.start()

def stop_scraping_func():
    global stop_scraping
    stop_scraping = True

if __name__ == "__main__":
    scraped= scrape(URL)
    extracted_temperature= extract(scraped)
    date = datetime.datetime.now()
    formatted_date = date.strftime('%Y-%m-%d-%H-%M-%S')
    store(formatted_date,extracted_temperature)