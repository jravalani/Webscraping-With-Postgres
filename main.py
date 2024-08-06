import psycopg2
import requests
import selectorlib
import time
from send_email import send_email
import database_functions
from datetime import datetime


# establish connection
connection = psycopg2.connect(
    dbname="app10_webscrap",
    user="postgres",
    password="root",
    host="localhost",
    port=5432
)

URL = "https://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    content = response.text
    return content


def extract(content):
    extractor = selectorlib.Extractor.from_yaml_file("../app10_2_scraping_tours_sql/extract.yaml")
    # 'tours' can be any variable we want. I have written tours in my yaml file which is why I passed tours here. what
    # matters is the content inside tours variable inside the yaml file. in this case it is css: '#displaytimer' <--
    # a css id, so the below code will extract the value from the element with that id
    value = extractor.extract(content)["tours"]
    return value


if __name__ == "__main__":
    while True:
        extracted = extract(scrape(URL))
        print(extracted)
        if extracted != 'No upcoming tours':
            row = database_functions.read(extracted)
            if not row:
                database_functions.store(extracted)
                try:
                    send_email(message=f"Hey, a new event was showed up!\n\n{extracted}")
                    print("Email Sent Successfully!")
                except Exception as e:
                    print(f"An error as occurred: {e}")
        time.sleep(10)
