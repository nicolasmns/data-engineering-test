import pandas as pd
import pytest
import os
from src.task_1_crate_distribution import *

def locate_test_file(filename: str):
    """Function that return the file along the path for the test resources directory"""
    return os.path.join(os.path.dirname(__file__), f"resources/{filename}")


@pytest.fixture
def sample_orders_data():
    """Datos de muestra para probar la carga del archivo CSV."""
    data = {
        "order_id": ["1", "2", "3"],
        "company_name": ["A", "A", "B"],
        "crate_type": ["Plastic", "Wood", "Metal"],
        "contact_data": ["[{ 'contact_name': 'John', 'contact_surname': 'Doe' }]", 
                         "[{ 'contact_name': 'Alice', 'contact_surname': 'Smith' }]", 
                         "[{ 'contact_name': 'Bob', 'contact_surname': 'Johnson' }]"],
        "salesowners": ["Owner1, Owner2", "Owner2, Owner3", "Owner1"]
    }
    return pd.DataFrame(data)

def test_load_csv_to_dataframe_valid_file():
    file_path = locate_test_file("sample.csv")
    df = load_csv_to_dataframe(file_path)
    assert isinstance(df, pd.DataFrame), "Returns a DataFrame"
    assert not df.empty, "Dateframe shouldn't be empty."

def test_load_csv_to_dataframe_empty_file():
    file_path = locate_test_file("empty_sample.csv")
    with pytest.raises(pd.errors.EmptyDataError, match="The file is empty or has no data to parse."):
        load_csv_to_dataframe(file_path)

def test_load_csv_to_dataframe_invalid_separator():
    file_path = locate_test_file("invalid_sep_sample.csv")
    with pytest.raises(pd.errors.ParserError, match="The file has an invalid separator or is malformed."):
        load_csv_to_dataframe(file_path)

def test_load_csv_to_dataframe_missing_columns():
    file_path = locate_test_file("missing_columns_sample.csv")
    with pytest.raises(ValueError, match="Missing columns:"):
        load_csv_to_dataframe(file_path)

def test_load_csv_to_dataframe_unexpected_columns():
    file_path = locate_test_file("unexpected_columns_sample.csv")
    with pytest.raises(ValueError, match="Unexpected columns:"):
        load_csv_to_dataframe(file_path)

def test_load_csv_to_dataframe_non_existent_file():
    file_path = locate_test_file("this_file_doesn't_exist.csv")
    with pytest.raises(FileNotFoundError):
        load_csv_to_dataframe(file_path)


def test_calculate_crate_distribution(sample_orders_data):
    """Verifies the distribution of orders for crater type by company_name"""
    expected_output = {
        "A": {"Metal":0, "Plastic": 1, "Wood": 1},
        "B": {"Metal":1, "Plastic": 0, "Wood": 0}
    }
    expected_df = pd.DataFrame(expected_output).T

    # The index for the expected output should match the dataframe
    expected_df.index.name = "company_name"
    expected_df.columns.name = "crate_type" 

    result = calculate_crate_distribution(sample_orders_data)
    pd.testing.assert_frame_equal(result, expected_df)

def test_calculate_crate_distribution_missing_values():
    ''' Verifies that the missing values like company_name or crater_type are properly handle

        Missing crater type record will be removed
        Missing company_name will be set to 'Unknown'
        If crater_type doesn't exist in the whole dataset, the column will be initialized as 0 for all records.
    '''
    data_with_missing = pd.DataFrame({
        "order_id": ["1", "2", "3"],
        "company_name": ["A", None, "B"],
        "crate_type": ["Plastic", "Wood", None],
    })
    result = calculate_crate_distribution(data_with_missing)

    expected_output = {
        "A": {"Metal":0, "Plastic": 1, "Wood": 0},
        "Unknown": {"Metal":0, "Plastic": 0, "Wood": 1}
    }
    expected_df = pd.DataFrame(expected_output).T

    # The index for the expected output should match the dataframe
    expected_df.index.name = "company_name"
    expected_df.columns.name = "crate_type" 

    pd.testing.assert_frame_equal(result, expected_df)

def test_calculate_crate_distribution_multiple_orders():
    """Validates that the function handles multiple orders of the same crate type correctly."""
    data = pd.DataFrame({
        "order_id": ["1", "2", "3", "4", "5"],
        "company_name": ["A", "A", "A", "B", "B"],
        "crate_type": ["Plastic", "Plastic", "Wood", "Metal", "Metal"],
    })
    result = calculate_crate_distribution(data)

    expected_output = {
        "A": {"Metal": 0, "Plastic": 2, "Wood": 1},
        "B": {"Metal": 2, "Plastic": 0, "Wood": 0},
    }
    expected_df = pd.DataFrame(expected_output).T

    # Ensure the index and column names match the expected format
    expected_df.index.name = "company_name"
    expected_df.columns.name = "crate_type"

    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_crate_distribution_missing_crate_types():
    """Ensures companies with no orders for a crate type have a count of 0."""
    data = pd.DataFrame({
        "order_id": ["1", "2", "3"],
        "company_name": ["A", "B", "A"],
        "crate_type": ["Plastic", "Wood", "Metal"],
    })
    result = calculate_crate_distribution(data)

    expected_output = {
        "A": {"Metal": 1, "Plastic": 1, "Wood": 0},
        "B": {"Metal": 0, "Plastic": 0, "Wood": 1},
    }
    expected_df = pd.DataFrame(expected_output).T

    # Ensure the index and column names match the expected format
    expected_df.index.name = "company_name"
    expected_df.columns.name = "crate_type"

    pd.testing.assert_frame_equal(result, expected_df)

def test_calculate_crate_distribution_all_null_company_name():
    """Validates that rows with null company_name are assigned to 'Unknown'."""
    data = pd.DataFrame({
        "order_id": ["1", "2", "3"],
        "company_name": [None, None, None],
        "crate_type": ["Plastic", "Metal", "Wood"],
    })
    result = calculate_crate_distribution(data)

    expected_output = {
        "Unknown": {"Metal": 1, "Plastic": 1, "Wood": 1},
    }
    expected_df = pd.DataFrame(expected_output).T

    # Ensure the index and column names match the expected format
    expected_df.index.name = "company_name"
    expected_df.columns.name = "crate_type"

    pd.testing.assert_frame_equal(result, expected_df)
