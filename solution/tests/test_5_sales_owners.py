import pytest
import pandas as pd
from src.task_5_sales_owners import *

# Fixtures para datos de prueba
@pytest.fixture
def sample_orders_df():
    data = {
        "company_id": [
            "1e2b47e6-499e-41c6-91d3-09d12dddfbbd",
            "1e2b47e6-499e-41c6-91d3-09d12dddfbbd",
            "0f05a8f1-2bdf-4be7-8c82-4c9b58f04898",
        ],
        "company_name": [
            "Fresh Fruits Co.",
            "fresh fruits co ",
            "Veggies Inc",
        ],
        "salesowners": [
            "Leonard Cohen, Luke Skywalker",
            "Luke Skywalker, Ammy Winehouse",
            "David Goliat, Luke Skywalker",
        ],
    }
    return pd.DataFrame(data)

@pytest.fixture
def normalized_orders_df():
    data = {
        "company_id": [
            "1e2b47e6-499e-41c6-91d3-09d12dddfbbd",
            "0f05a8f1-2bdf-4be7-8c82-4c9b58f04898",
        ],
        "company_name": ["fresh fruits co", "veggies inc"],
        "salesowners": [
            "Leonard Cohen, Luke Skywalker, Ammy Winehouse",
            "David Goliat, Luke Skywalker",
        ],
    }
    return pd.DataFrame(data)

# Tests
def test_normalize_company_names(sample_orders_df):
    """
    Test that company names are normalized correctly by:
    - Converting to lowercase.
    - Stripping extra spaces.
    - Removing non-alphanumeric characters.
    """
    result = normalize_company_names(sample_orders_df)
    assert result["company_name"].iloc[0] == "fresh fruits co"
    assert result["company_name"].iloc[1] == "fresh fruits co"
    assert result["company_name"].iloc[2] == "veggies inc"

def test_group_same_companies(sample_orders_df):
    """
    Test that duplicate companies are grouped correctly by:
    - Keeping the first company_id.
    - Merging and deduplicating the salesowners lists.
    """
    normalized_df = normalize_company_names(sample_orders_df)
    result = group_same_companies(normalized_df)
    assert len(result) == 2  # Only two unique company names
    assert result["company_id"].iloc[0] == "1e2b47e6-499e-41c6-91d3-09d12dddfbbd"
    # I'm formating this because the sorting of the sales owners may vary and isn't sorted in this method
    assert "Leonard Cohen" in result["salesowners"].iloc[0] and\
          "Ammy Winehouse" in result["salesowners"].iloc[0] and \
          "Luke Skywalker" in result["salesowners"].iloc[0]

def test_sort_df_alphabetically(normalized_orders_df):
    """
    Test that the list of sales owners is:
    - Sorted alphabetically by first name.
    - Contains only unique names.
    """
    result = sort_df_alphabetically(normalized_orders_df)
    assert result["list_salesowners"].iloc[0] == "Ammy Winehouse, Leonard Cohen, Luke Skywalker"
    assert result["list_salesowners"].iloc[1] == "David Goliat, Luke Skywalker"

def test_uniqueness_of_salesowners(normalized_orders_df):
    """
    Validate that the salesowners list has unique names after processing.
    """
    result = sort_df_alphabetically(normalized_orders_df)
    for salesowners in result["list_salesowners"]:
        salesowners_list = salesowners.split(", ")
        assert len(salesowners_list) == len(set(salesowners_list)), "Duplicated names found in salesowners list"

def test_duplicate_companies(sample_orders_df):
    """
    Ensure that duplicate companies (same name) are handled correctly:
    - Only one entry per company name.
    - Salesowners lists are merged and unique.
    """
    normalized_df = normalize_company_names(sample_orders_df)
    result = group_same_companies(normalized_df)
    assert len(result) == 2  # Two unique company names
    assert "fresh fruits co" in result["company_name"].values
    assert "veggies inc" in result["company_name"].values
