import pandas as pd
import psycopg2
import subprocess
from src.task_4.load_data import load_data_to_postgres
import src.utils as utils
import sys

#######################################################################################################################
# Test 4: Calculation of Sales Team Commissions                                                                       #
#                                                                                                                     #
# The Sales Team requires your assistance in computing the commissions. It is possible for multiple salespersons      #
# to be associated with a single order, as they may have participated in different stages of the order. The           #
# `salesowners` field comprises a ranked list of the salespeople who have ownership of the order. The first           #
# individual on the list represents the primary owner, while the subsequent individuals, if any, are considered       #
# co-owners who have contributed to the acquisition process. The calculation of commissions follows a specific        #
# procedure:                                                                                                          #
#                                                                                                                     #
# - Main Owner: 6% of the net invoiced value.                                                                         #
# - Co-owner 1 (second in the list): 2.5% of the net invoiced value.                                                  #
# - Co-owner 2 (third in the list): 0.95% of the net invoiced value.                                                  #
# - The rest of the co-owners do not receive anything.                                                                #
#                                                                                                                     #
# Provide a list of the distinct sales owners and their respective commission earnings. The list should be sorted in  #
# order of descending performance, with the sales owners who have generated the highest commissions appearing first.  #
#                                                                                                                     #
# Hint: Raw amounts are represented in cents. Please provide euro amounts with two decimal places in the results.     #
#######################################################################################################################


VIEW_NAME = "calculate_comissions"

def run_dbt():
    """
    Executes the dbt run command to materialize the transformations.
    """
    try:

        dbt_dir = utils.getDbtpath()

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
        # Annoying warning that suggests to use sql alchemy and create an engine to fetch the table.
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable.*")
            df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching results: {e}")
        return None

def main():
    try:
        load_data_to_postgres(utils.HOST, None)
        run_dbt()
        df = fetch_dbt_results(utils.HOST, view_name=VIEW_NAME)
        if df is not None:
            print(df)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__=='__main__':
    main()