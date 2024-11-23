import psycopg2
import pandas as pd
from src.utils import getFilepath
from datetime import datetime
from json.decoder import JSONDecodeError
import json

import os


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
    Handles empty or null contact data values.

    Args:
        value (str): Contact data input.

    Returns:
        str: The input value if not empty or None, otherwise an empty string.
    """
    return "" if pd.isna(value) or value == "" else value

def load_data_to_postgres(host, test_path):
    """
    Connects to a PostgreSQL database and loads data from orders.csv and invoicing_data.json.
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
            # Determine file paths
            if test_path is None:
                orders_filepath = getFilepath(ORDER_FILE)
                invoicing_filepath = getFilepath(INVOICING_FILE)
            else:
                orders_filepath = test_path[0]
                invoicing_filepath = test_path[1]

            # Load orders file
            try:
                orders_df = pd.read_csv(orders_filepath, sep=";")
                if orders_df.empty:
                    raise Exception("orders.csv is empty.")
            except pd.errors.EmptyDataError:
                raise Exception("orders.csv is empty.")
            except pd.errors.ParserError as e:
                raise Exception(f"Error parsing orders.csv: {e}")
            except FileNotFoundError:
                raise FileNotFoundError(f"Orders file not found: {orders_filepath}")

            # Validate required columns
            required_columns = ["order_id", "date", "company_id", "company_name", "crate_type", "contact_data", "salesowners"]
            missing_columns = [col for col in required_columns if col not in orders_df.columns]
            if missing_columns:
                raise Exception(f"Missing required columns in orders.csv: {missing_columns}")

            # Process and insert data into the database
            orders_df["date"] = orders_df["date"].apply(convert_date)
            orders_df["contact_data"] = orders_df["contact_data"].apply(clean_contact_data)

            insert_query = """
                INSERT INTO orders (order_id, date, company_id, company_name, crate_type, contact_data, salesowners)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, [
                (row["order_id"], row["date"], row["company_id"], row["company_name"], row["crate_type"],
                 row["contact_data"], row["salesowners"])
                for _, row in orders_df.iterrows()
            ])
            print("Orders.csv data loaded successfully!")

            # Load invoicing file
            try:
                with open(invoicing_filepath, "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                raise FileNotFoundError(f"Invoicing file not found: {invoicing_filepath}")

            # Validate JSON keys
            invoicing_data = data.get("data", {}).get("invoices", [])
            if not invoicing_data:
                raise Exception("No invoices found in invoicing_data.json.")
            required_keys = ["id", "orderId", "companyId", "grossValue", "vat"]
            for key in required_keys:
                if key not in invoicing_data[0]:
                    raise Exception(f"Missing required key '{key}' in invoicing_data.json.")

            # Process and insert invoicing data
            try:
                invoicing_df = pd.DataFrame(invoicing_data)
            except FileNotFoundError:
                raise Exception(f"Invoicing file not found: {invoicing_filepath}")
            invoicing_query = """
                INSERT INTO invoicing_data (id, order_id, company_id, gross_value, vat)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(invoicing_query, [
                (row["id"], row["orderId"], row["companyId"], row["grossValue"], row["vat"])
                for _, row in invoicing_df.iterrows()
            ])
            print("Invoicing_data.json data loaded successfully!")

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Error while loading data: {e}")
            raise e

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e
