from datetime import datetime
import psycopg2

connection = psycopg2.connect(
    dbname="app10_webscrap",
    user="postgres",
    password="root",
    host="localhost",
    port=5432
)

def store(extracted):
    value = extracted.split(",")
    value = [item.strip() for item in value]
    band, city, raw_date = value
    raw_date_object = datetime.strptime(raw_date, '%d.%m.%Y')
    date = raw_date_object.strftime('%Y-%m-%d')
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO scrapped_data (band, city, date) VALUES(%s, %s, %s)", (band, city, date))
        connection.commit()
        print("Data successfully inserted into the database")
    except psycopg2.Error as e:
        print(f"An error as occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()


def read(extracted):
    value = extracted.split(",")
    value = [item.strip() for item in value]
    band, city, raw_date = value
    raw_date_object = datetime.strptime(raw_date, '%d.%m.%Y')
    date = raw_date_object.strftime('%Y-%m-%d')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM scrapped_data WHERE band=%s AND city=%s AND date=%s", (band, city, date))
        rows = cursor.fetchall()
        print("Successfully extracted values from the database")
    except psycopg2.Error as e:
        print(f"An error as occurred while reading values: {e}")
    finally:
        cursor.close()

    print(rows)
    return rows