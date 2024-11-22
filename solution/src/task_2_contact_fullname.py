from src.task_1_crate_distribution import load_csv_to_dataframe
from src.utils import getFilepath
import pandas as pd
import ast
import os


#######################################################################################################################
# Test 2: DataFrame of Orders with Full Name of the Contact                                                           #
# Provide a DataFrame (df_1) containing the following columns:                                                        #
# ------------------------------------------------------------------------------------------------                    #
# | Column	            | Description                                                            |                    #
# |---------------------|------------------------------------------------------------------------|                    #
# | order_id	        | The order_id field must contain the unique identifier of the order.    |                    #
# |---------------------|------------------------------------------------------------------------|                    #
# | contact_full_name	| The contact_full_name field must contain the full name of the contact. |                    #
# ----------------------|-------------------------------------------------------------------------                    #
# ##################################################################################################################### 

def extract_contact_full_name(contact_data):
    """
    Extracts the full name of the contact from the contact_data column.
    If the contact data is missing, malformed, or incomplete, returns "John Doe".

    Args:
        contact_data: A string representing the contact data in a list with a single element with JSON-like format.

    Returns:
        str: Full name of the contact or "John Doe" if missing or invalid.
    """
    try:
        # Convert the string to a List Object
        parsed_data = ast.literal_eval(contact_data) if isinstance(contact_data, str) else None

        # Ensure the parsed data is a list and has at least one element
        if isinstance(parsed_data, list) and parsed_data:
            contact = parsed_data[0]
            name = contact.get("contact_name", "").strip()
            surname = contact.get("contact_surname", "").strip()
            
            if name and surname:
                return f"{name} {surname}"
    except (ValueError, SyntaxError, TypeError):
        pass  # If parsing fails or contact_data is invalid, fall back to the default name which is "John Doe"

    return "John Doe"

def create_orders_with_contact_names(raw_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame containing order_id and contact_full_name.

    Args:
        raw_dataframe: pd.DataFrame containing raw order data.

    Returns:
        pd.DataFrame: A DataFrame with order_id and contact_full_name columns.
    """

    raw_dataframe["contact_full_name"] = raw_dataframe["contact_data"].apply(extract_contact_full_name)

    return raw_dataframe[["order_id", "contact_full_name"]]

def main():
    orders_filepath = getFilepath("orders.csv")
    df_1 = create_orders_with_contact_names(load_csv_to_dataframe(orders_filepath))
    print(df_1)

if __name__ == '__main__':
    main()