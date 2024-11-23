from src.utils import getFilepath
import os
import pandas as pd
import json


#######################################################################################################################
# Test 5: DataFrame of Companies with Sales Owners                                                                    #
#                                                                                                                     #
# Provide a DataFrame (df_3) containing the following columns:                                                        #
# ------------------------------------------------------------------------------------------------                    #
# | Column              | Description                                                            |                    #
# |---------------------|------------------------------------------------------------------------|                    #
# | company_id          | The company_id field must contain the unique identifier of the company.|                    #
# |---------------------|------------------------------------------------------------------------|                    #
# | company_name        | The company_name field must contain the name of the company.           |                    #
# |---------------------|------------------------------------------------------------------------|                    #
# | list_salesowners    | The list_salesowners field should contain a unique and comma-separated |                    #
# |                     | list of salespeople who have participated in at least one order of the |                    #
# |                     | company. Please ensure that the list is sorted in ascending            |                    #
# |                     | alphabetical order of the first name.                                  |                    #
# ------------------------------------------------------------------------------------------------                    #
#                                                                                                                     #
# Hint: Consider the possibility of duplicate companies stored under multiple IDs in the database. Take this into     #
# account while devising a solution to this exercise.                                                                 #
#                                                                                                                     #                                                                                                #
#######################################################################################################################

def normalize_company_names(df):
    """
    Normalize company names by making them lowercase and removing any characters
    that are not a word or a space.

    Args:
        df (pd.DataFrame): The DataFrame containing a 'company_name' column to be normalized.

    Returns:
        pd.DataFrame: The DataFrame with normalized 'company_name' values.
    """
    df["company_name"] = df["company_name"].str.lower().str.strip()
    df["company_name"] = df["company_name"].str.replace(r"[^\w\s]", "", regex=True)
    return df

def group_same_companies(df):
    """
    Group companies with the same normalized name. If two companies have the same 
    name, take the first company ID and combine the list of sales owners, sales owners
    won't be duplicated in the list

    Args:
        df (pd.DataFrame): The DataFrame containing 'company_name', 'company_id',
                           and 'salesowners' columns.

    Returns:
        pd.DataFrame: A DataFrame with unique company names, the first company ID,
                      and a combined list of sales owners for each company.
    """
    unique_companies = df.groupby("company_name").agg({
        "company_id": "first",
        "salesowners": lambda x: ", ".join(set(", ".join(x.dropna()).split(", ")))
    }).reset_index()
    return unique_companies

def load_orders_file(filepath):
    """
    Load the orders file from the filepath

    Args:
        filepath (str): The relative or absolute path to the orders CSV file

    Returns:
        pd.DataFrame: The loaded DataFrame from the CSV file
    """
    orders_file = getFilepath(filepath)
    return pd.read_csv(orders_file, sep=";")

def sort_df_alphabetically(df):
    """
    Sort the list of sales owners alphabetically within each row

    Args:
        df (pd.DataFrame): The DataFrame containing a salesowners column

    Returns:
        pd.DataFrame: The DataFrame with an added or updated 'list_salesowners' column,
                      where sales owners are unique and sorted alphabetically
    """
    df["list_salesowners"] = df["salesowners"].apply(
        lambda x: ", ".join(sorted(set(x.split(", "))))
    )
    return df

def generate_list_sales_owners():
    """
    Generate a DataFrame containing unique companies with their normalized names,
    the first company ID, and a sorted list of sales owners.

    Returns:
        pd.DataFrame: A DataFrame with columns 'company_id', 'company_name',
                      and 'list_salesowners'
    """
    orders_df = load_orders_file("orders.csv")
    orders_df = normalize_company_names(orders_df)
    unique_companies = group_same_companies(orders_df)
    sort_df_alphabetically(unique_companies)
    return unique_companies[["company_id", "company_name", "list_salesowners"]]

if __name__ == '__main__':
    df3 = generate_list_sales_owners()
    print(df3)

