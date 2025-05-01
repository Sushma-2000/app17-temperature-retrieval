import datetime
import threading
import time
import sqlite3
import requests
import selectorlib
import pandas as pd

# Constants
URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# Thread control variable
stop_scraping = False

def get_connection():
    """Create a thread-safe SQLite connection."""
    return sqlite3.connect("data.db", check_same_thread=False)

def init_db():
    """Initialize the database and create the table if not exists."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperature_store (
        date TEXT,
        temperature INTEGER
    )
    """)
    conn.commit()
    conn.close()

def scrape(url):
    """Scrape the page source from URL."""
    response = requests.get(url, headers=HEADERS)
    return response.text

def extract(source):
    """Extract temperature using selectorlib."""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["temperature"]
    return value

def store(date_now, temperature):
    """Store the extracted data into the SQLite database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO temperature_store VALUES (?, ?)", (date_now, temperature))
    conn.commit()
    conn.close()

def read_content():
    """Read the stored temperature data and return as a DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM temperature_store", conn)
    conn.close()
    return df

def put_data():
    """Scrape, extract and store a single temperature record."""
    try:
        print("Storing data...")
        scraped = scrape(URL)
        extracted_temperature = extract(scraped)
        date = datetime.datetime.now()
        formatted_date = date.strftime('%Y-%m-%d-%H-%M-%S')
        store(formatted_date, extracted_temperature)
    except Exception as e:
        print(f"Error during scraping: {e}")

def start_scraping():
    """Start the background scraping thread."""
    global scraping_thread, stop_scraping
    stop_scraping = False

    def run():
        while not stop_scraping:
            put_data()
            time.sleep(5)  # scrape every 5 seconds

    scraping_thread = threading.Thread(target=run)
    scraping_thread.start()

def stop_scraping_func():
    """Signal the scraping thread to stop."""
    global stop_scraping
    stop_scraping = True

# Initialize DB on import
init_db()

# Optional manual run
if __name__ == "__main__":
    put_data()