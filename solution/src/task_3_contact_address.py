from src.task_1_crate_distribution import load_csv_to_dataframe
import pandas as pd
import ast
import os

#######################################################################################################################
# Test 3: DataFrame of Orders with Contact Address                                                                    #
# Provide a DataFrame (df_2) containing the following columns:                                                        #
#                                                                                                                     #
# --------------------------------------------------------------------------------------------------                  #
# | Column           | Description                                                                 |                  #
# |------------------------------------------------------------------------------------------------|                  #
# | order_id         | The order_id field must contain the unique identifier of the order.         |                  #
# |------------------------------------------------------------------------------------------------|                  #
# | contact_address  | The field for contact_address should adhere to the following information    |                  #
# |                  | and format: "city name, postal code". If the city name is not available,    |                  #
# |                  | the placeholder "Unknown" should be used. Similarly, if the postal code     |                  #
# |                  | is not known, the placeholder "UNK00" should be used.                       |                  #
# --------------------------------------------------------------------------------------------------                  #
#######################################################################################################################

def extract_city_and_postal_code(contact_data):
    """
    Extracts the city name and postal code from the contact_data column.
    If the contact data is missing, malformed, or incomplete, returns ["Unknown", "UNK00"].

    Args:
        contact_data: A string representing the contact data in a JSON-like format (list or dict).

    Returns:
        list: A list with [city_name, postal_code] or ["Unknown", "UNK00"] if missing or invalid.
    """
    try:
        parsed_data = ast.literal_eval(contact_data) if isinstance(contact_data, str) else None

        if isinstance(parsed_data, list) and parsed_data:
            contact = parsed_data[0]
        elif isinstance(parsed_data, dict):
            contact = parsed_data
        else:
            return "Unknown, UNK00"

        city = contact.get("city", "Unknown").strip()
        postal_code = str(contact.get("cp", "UNK00")).strip()

        # If the city name is only numbers or contains spaces, then it's invalid.
        if len(city) == 0 or city.isdigit():
            city = "Unknown"

        # If the postal code is only spaces, or isn't alphanumeric (or numeric) or if it's alphanumeric but only contains words, then it's invalid.
        if len(postal_code) == 0 or not postal_code.isalnum() or postal_code.isalpha():
            postal_code = "UNK00"

        return f"{city}, {postal_code}"

    except (ValueError, SyntaxError, TypeError):
        pass

    return "Unknown, UNK00"

def create_orders_with_contact_address(processed_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame containing order_id and contact_full_name.

    Args:
        raw_dataframe: pd.DataFrame containing raw order data.

    Returns:
        pd.DataFrame: A DataFrame with order_id and contact_full_name columns.
    """
    processed_dataframe["contact_address"] = processed_dataframe["contact_data"].apply(extract_city_and_postal_code)

    return processed_dataframe[["order_id", "contact_address"]]

def main():
    orders_filepath = os.path.join(os.path.dirname(__file__), "../../resources/orders.csv")
    df_2 = create_orders_with_contact_address(load_csv_to_dataframe(orders_filepath))
    print(df_2)

if __name__ == '__main__':
    main()