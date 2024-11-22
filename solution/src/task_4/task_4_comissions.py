import pandas as pd
import psycopg2
import subprocess
from src.task_4.load_data import load_data_to_postgres
from src.utils import getDbtpath
import os

HOST = "localhost"
VIEW_NAME = "calculate_comissions"

def run_dbt():
    """
    Executes the dbt run command to materialize the transformations.
    """
    try:

        dbt_dir = getDbtpath()

        result = subprocess.run(
            ["dbt", "run", "--profiles-dir", dbt_dir, "--project-dir", dbt_dir],
            capture_output=True,
            text=True,
            check=True
        )
        print("DBT command executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running dbt command.")
        print(e.stderr)

def fetch_dbt_results(host, view_name="your_dbt_view_or_table"):
    """
    Fetches the results of the DBT model from the database.
    Args:
        host: str of the host where the view is stored
    
    Returns:
        df: pd.Dataframe of the view
    """
    try:
        conn = psycopg2.connect(
            dbname="data_engineering_test",
            user="user",
            password="password",
            host=host,
            port="5432"
        )
        query = f"SELECT * FROM {view_name}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching results: {e}")
        return None


def main():
    try:
        load_data_to_postgres(HOST)
        run_dbt()
        df = fetch_dbt_results(HOST, view_name=VIEW_NAME)
        if df is not None:
            print(df)
    except:
        raise "Something failed."

if __name__=='__main__':
    main()