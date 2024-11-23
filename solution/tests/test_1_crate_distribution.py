import pandas as pd
import pytest
import os
from src.task_1_crate_distribution import *
from tests.utils import locate_test_file

# @pytest.fixture
# def locate_test_file():
#     """Helper to locate test resource files."""
#     def _locate(filename):
#         return os.path.join(os.path.dirname(__file__), f"resources/{filename}")
#     return _locate


@pytest.fixture
def create_expected_dataframe():
    """Helper to create expected DataFrames with consistent index and column names."""
    def _create_expected(data):
        df = pd.DataFrame(data).T
        df.index.name = "company_name"
        df.columns.name = "crate_type"
        return df
    return _create_expected


@pytest.fixture
def sample_orders_data():
    """Sample data for testing."""
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


def validate_dataframe_format(df, expected_index_name, expected_column_name):
    """Validates the format of a DataFrame."""
    assert df.index.name == expected_index_name, f"Index name should be '{expected_index_name}'"
    assert df.columns.name == expected_column_name, f"Column name should be '{expected_column_name}'"


def test_load_csv_to_dataframe_valid_file():
    file_path = locate_test_file("sample.csv")
    df = load_csv_to_dataframe(file_path)
    assert isinstance(df, pd.DataFrame), "Should return a DataFrame"
    assert not df.empty, "DataFrame should not be empty."


def test_load_csv_to_dataframe_empty_file():
    file_path = locate_test_file("empty_sample.csv")
    with pytest.raises(pd.errors.EmptyDataError):
        load_csv_to_dataframe(file_path)


def test_load_csv_to_dataframe_invalid_separator():
    file_path = locate_test_file("invalid_sep_sample.csv")
    with pytest.raises(pd.errors.ParserError):
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


def test_calculate_crate_distribution(sample_orders_data, create_expected_dataframe):
    expected_data = {
        "A": {"Metal": 0, "Plastic": 1, "Wood": 1},
        "B": {"Metal": 1, "Plastic": 0, "Wood": 0},
    }
    expected_df = create_expected_dataframe(expected_data)
    result = calculate_crate_distribution(sample_orders_data)

    validate_dataframe_format(result, "company_name", "crate_type")
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_crate_distribution_missing_values(create_expected_dataframe):
    data_with_missing = pd.DataFrame({
        "order_id": ["1", "2", "3"],
        "company_name": ["A", None, "B"],
        "crate_type": ["Plastic", "Wood", None],
    })
    expected_data = {
        "A": {"Metal": 0, "Plastic": 1, "Unknown Crate": 0, "Wood": 0},
        "B": {"Metal": 0, "Plastic": 0, "Unknown Crate": 1, "Wood": 0},
        "Unknown": {"Metal": 0, "Plastic": 0, "Unknown Crate": 0, "Wood": 1},
    }
    expected_df = create_expected_dataframe(expected_data)
    result = calculate_crate_distribution(data_with_missing)

    validate_dataframe_format(result, "company_name", "crate_type")
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_crate_distribution_multiple_orders(create_expected_dataframe):
    data = pd.DataFrame({
        "order_id": ["1", "2", "3", "4", "5"],
        "company_name": ["A", "A", "A", "B", "B"],
        "crate_type": ["Plastic", "Plastic", "Wood", "Metal", "Metal"],
    })
    expected_data = {
        "A": {"Metal": 0, "Plastic": 2, "Wood": 1},
        "B": {"Metal": 2, "Plastic": 0, "Wood": 0},
    }
    expected_df = create_expected_dataframe(expected_data)
    result = calculate_crate_distribution(data)

    validate_dataframe_format(result, "company_name", "crate_type")
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_crate_distribution_missing_crate_types(create_expected_dataframe):
    data = pd.DataFrame({
        "order_id": ["1", "2", "3"],
        "company_name": ["A", "B", "A"],
        "crate_type": ["Plastic", "Wood", "Metal"],
    })
    expected_data = {
        "A": {"Metal": 1, "Plastic": 1, "Wood": 0},
        "B": {"Metal": 0, "Plastic": 0, "Wood": 1},
    }
    expected_df = create_expected_dataframe(expected_data)
    result = calculate_crate_distribution(data)

    validate_dataframe_format(result, "company_name", "crate_type")
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_crate_distribution_additional_crate_types(create_expected_dataframe):
    data = pd.DataFrame({
        "order_id": ["1", "2", "3", "4"],
        "company_name": ["A", "A", "B", "B"],
        "crate_type": ["Plastic", "Fiberglass", "Wood", "Cardboard"],
    })
    expected_data = {
        "A": {"Cardboard": 0, "Fiberglass": 1, "Metal": 0, "Plastic": 1, "Wood": 0},
        "B": {"Cardboard": 1, "Fiberglass": 0, "Metal": 0, "Plastic": 0, "Wood": 1},
    }
    expected_df = create_expected_dataframe(expected_data)
    result = calculate_crate_distribution(data)

    validate_dataframe_format(result, "company_name", "crate_type")
    pd.testing.assert_frame_equal(result, expected_df)

def test_calculate_crate_distribution_all_null_company_name(create_expected_dataframe):
    """Validates that rows with null company_name are assigned to 'Unknown'."""
    data = pd.DataFrame({
        "order_id": ["1", "2", "3"],
        "company_name": [None, None, None],
        "crate_type": ["Plastic", "Metal", "Wood"],
    })

    expected_output = {
        "Unknown": {"Metal": 1, "Plastic": 1, "Wood": 1},
    }
    expected_df = create_expected_dataframe(expected_output)
    result = calculate_crate_distribution(data)

    pd.testing.assert_frame_equal(result, expected_df)

def test_calculate_crate_distribution_mixed_nulls_and_additional(create_expected_dataframe):
    """Validates handling of mixed nulls and additional crate types."""
    data = pd.DataFrame({
        "order_id": ["1", "2", "3", "4", "5"],
        "company_name": ["A", "B", "B", None, "C"],
        "crate_type": ["Plastic", "Wood", None, "Fiberglass", "Plastic"],
    })

    expected_output = {
        "A": {"Fiberglass": 0, "Metal": 0, "Plastic": 1, "Unknown Crate": 0, "Wood": 0},
        "B": {"Fiberglass": 0, "Metal": 0, "Plastic": 0, "Unknown Crate": 1, "Wood": 1},
        "C": {"Fiberglass": 0, "Metal": 0, "Plastic": 1, "Unknown Crate": 0, "Wood": 0},
        "Unknown": {"Fiberglass": 1, "Metal": 0, "Plastic": 0, "Unknown Crate": 0, "Wood": 0},
    }
    expected_df = create_expected_dataframe(expected_output)
    result = calculate_crate_distribution(data)

    pd.testing.assert_frame_equal(result, expected_df)

def test_calculate_crate_distribution_duplicate_order_ids(create_expected_dataframe):
    """Test to ensure duplicate order_ids are dropped correctly."""
    data_with_duplicates = pd.DataFrame({
        "order_id": ["1", "1", "2", "3"],
        "company_name": ["A", "A", "B", "B"],
        "crate_type": ["Plastic", "Plastic", "Wood", "Metal"],
    })

    # Expected result after dropping duplicates
    expected_output = {
        "A": {"Metal": 0, "Plastic": 1, "Wood": 0},
        "B": {"Metal": 1, "Plastic": 0, "Wood": 1},
    }
    expected_df = create_expected_dataframe(expected_output)

    # Apply the function (dropping duplicates is part of the function's logic)
    result = calculate_crate_distribution(data_with_duplicates)

    # Assert the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result, expected_df)



