import pytest
import pandas as pd
from src.task_2_contact_fullname import create_orders_with_contact_names

def test_create_orders_with_multiple_entries():
    """
    Verifies the extraction of full names for orders with multiple entries, including valid and invalid data.
    """

    raw_data = {
        "order_id": [1, 2, 3],
        "contact_data": [
            '[{ "contact_name":"Curtis", "contact_surname":"Jackson", "city":"Chicago", "cp": "12345"}]',  
            '[{ "contact_name":"", "contact_surname":"Jackson", "city":"Chicago", "cp": "12345"}]',
            "invalid",
        ],
    }
    raw_df = pd.DataFrame(raw_data)

    expected_output = {
        "order_id": [1, 2, 3],
        "contact_full_name": ["Curtis Jackson", "John Doe", "John Doe"],
    }
    expected_df = pd.DataFrame(expected_output)

    result_df = create_orders_with_contact_names(raw_df)

    result_df.index.name = "index"
    expected_df.index.name = "index"

    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


def run_test_case(order_id, contact_data, expected_full_name):
    """
    Helper function to test a single case of create_orders_with_contact_names.
    """
    raw_data = {
        "order_id": [order_id],
        "contact_data": [contact_data],
    }
    raw_df = pd.DataFrame(raw_data)

    expected_output = {
        "order_id": [order_id],
        "contact_full_name": [expected_full_name],
    }
    expected_df = pd.DataFrame(expected_output)

    result_df = create_orders_with_contact_names(raw_df)

    pd.testing.assert_frame_equal(result_df, expected_df)


def test_valid_contact_data():
    """
    Verifies that valid contact data is correctly extracted.
    """
    run_test_case(
        order_id=1,
        contact_data='[{ "contact_name":"Curtis", "contact_surname":"Jackson", "city":"Chicago", "cp": "12345"}]',
        expected_full_name="Curtis Jackson",
    )


def test_missing_name():
    """
    Verifies that missing contact_name results in 'John Doe'.
    """
    run_test_case(
        order_id=2,
        contact_data='[{ "contact_name":"", "contact_surname":"Jackson", "city":"Chicago", "cp": "12345"}]',
        expected_full_name="John Doe",
    )


def test_invalid_structure():
    """
    Verifies that invalid JSON structure results in 'John Doe'.
    """
    run_test_case(
        order_id=3,
        contact_data="invalid",
        expected_full_name="John Doe",
    )


def test_only_spaces():
    """
    Verifies that spaces in contact_name and contact_surname result in 'John Doe'.
    """
    run_test_case(
        order_id=4,
        contact_data='[{ "contact_name":"   ", "contact_surname":"   ", "city":"Unknown", "cp": "00000"}]',
        expected_full_name="John Doe",
    )


def test_empty_json():
    """
    Verifies that an empty JSON results in 'John Doe'.
    """
    run_test_case(
        order_id=5,
        contact_data='[{}]',
        expected_full_name="John Doe",
    )


def test_null_values():
    """
    Verifies that null values in contact_name and contact_surname result in 'John Doe'.
    """
    run_test_case(
        order_id=6,
        contact_data='[{ "contact_name": null, "contact_surname": null, "city": "Somewhere"}]',
        expected_full_name="John Doe",
    )


def test_non_ascii_characters():
    """
    Verifies that contact_name and contact_surname with non-ASCII characters are handled correctly.
    """
    run_test_case(
        order_id=7,
        contact_data='[{ "contact_name":"张", "contact_surname":"伟", "city":"Beijing", "cp":"100000"}]',
        expected_full_name="张 伟",
    )


def test_misspelled_keys():
    """
    Verifies that misspelled keys result in 'John Doe'.
    """
    run_test_case(
        order_id=8,
        contact_data='[{ "contact_nam":"Alice", "contact_sur":"Wonderland"}]',
        expected_full_name="John Doe",
    )


def test_multiple_entries_in_list():
    """
    Verifies that only the first entry in the contact_data list is used.
    """
    run_test_case(
        order_id=9,
        contact_data='[{ "contact_name":"John", "contact_surname":"Smith"}, { "contact_name":"Bob", "contact_surname":"Builder"}]',
        expected_full_name="John Smith",
    )


def test_completely_empty():
    """
    Verifies that completely empty contact_data results in 'John Doe'.
    """
    run_test_case(
        order_id=10,
        contact_data="",
        expected_full_name="John Doe",
    )
