import psycopg2
import pandas as pd
import os
from src.utils import getFilepath
from datetime import datetime
import json

ORDER_FILE = "orders.csv"
INVOICING_FILE = "invoicing_data.json"

def convert_date(date_string):
    """
    Converts a date string from the format 'DD.MM.YY' to 'YYYY-MM-DD'.

    Args:
        date_string (str): A date string in the format 'DD.MM.YY'.

    Returns:
        str: The converted date string in the format 'YYYY-MM-DD'. 
        Returns None if the input format is invalid or conversion fails.
    """
    try:
        date_object = datetime.strptime(date_string, "%d.%m.%y")
        return date_object.strftime("%Y-%m-%d")
    except ValueError:
        return None
   
def clean_contact_data(value):
    """
    Cleans and formats the contact data.

    Args:
        value (str): A JSON-formatted string or other input representing contact data.

    Returns:
        str: A cleaned and properly formatted JSON string. If the input is empty or invalid, 
        returns an empty string or the string representation of the input.
    """
    if pd.isna(value) or value == "":
        return ""
    try:
        parsed_value = json.loads(value)  
        return json.dumps(parsed_value)
    except (json.JSONDecodeError, TypeError):
        return str(value)

def load_data_to_postgres(host):
    """
    This method connects to a PostgreSQL database and loads data from two sources:
    - orders.csv: Inserts order data into the 'orders' table.
    - invoicing_data.json: Inserts invoicing data into the 'invoicing_data' table.
    It handles database connections and ensures all data is committed once successfully loaded.
    """
    try:
        conn = psycopg2.connect(
            dbname="data_engineering_test",
            user="user",
            password="password",
            host=host,
            port="5432"
        )
        cursor = conn.cursor()

        try:
            # Load orders file
            orders_filepath = getFilepath(ORDER_FILE)
            orders_df = pd.read_csv(orders_filepath, sep=";")

            # Convert date to YYYY-MM-DD
            orders_df["date"] = orders_df["date"].apply(convert_date)

            # 
            orders_df["contact_data"] = orders_df["contact_data"].apply(clean_contact_data)

            insert_query = """
                INSERT INTO orders (order_id, date, company_id, company_name, crate_type, contact_data, salesowners)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            print(f"Attempting to insert {len(orders_df)} records into orders table.")

            # Executemany is more efficient to insert records
            cursor.executemany(insert_query, [
                (row["order_id"], row["date"], row["company_id"], row["company_name"], row["crate_type"],
                 row["contact_data"], row["salesowners"])
                for _, row in orders_df.iterrows()
            ])
            print("Orders.csv data loaded successfully!")

            # Load invoicing file
            invoicing_filepath = getFilepath(INVOICING_FILE)

            with open(invoicing_filepath, "r") as file:
                data = json.load(file)

            invoices = data["data"]["invoices"]

            invoicing_df = pd.DataFrame(invoices)

            invoicing_query = """
                INSERT INTO invoicing_data (id, order_id, company_id, gross_value, vat)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.executemany(invoicing_query, [
                (row["id"], row["orderId"], row["companyId"], row["grossValue"], row["vat"])
                for _, row in invoicing_df.iterrows()
            ])

            conn.commit() 
            print("Invoicing_data loaded successfully")

        except Exception as e:
            conn.rollback()
            print(f"Error while loading data: {e}")
        
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error connecting to the database: {e}")

