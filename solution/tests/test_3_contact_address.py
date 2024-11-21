import pytest
import pandas as pd
from src.task_3_contact_address import create_orders_with_contact_address

def test_create_orders_with_multiple_addresses():
    """
    Verifies the creation of contact_address for multiple orders with various cases of valid and invalid data.
    """
    raw_data = {
        "order_id": [1, 2, 3],
        "contact_data": [
            '[{ "city": "Chicago", "cp": "12345" }]',
            '[{ "city": "New York" }]',
            "invalid",
        ],
    }
    raw_df = pd.DataFrame(raw_data)

    expected_output = {
        "order_id": [1, 2, 3],
        "contact_address": ["Chicago, 12345", "New York, UNK00", "Unknown, UNK00"],
    }
    expected_df = pd.DataFrame(expected_output)

    result_df = create_orders_with_contact_address(raw_df)

    result_df.index.name = "index"
    expected_df.index.name = "index"

    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


def run_test_case(order_id, contact_data, expected_address):
    """
    Helper function to test a single case of create_orders_with_contact_address.
    """
    raw_data = {
        "order_id": [order_id],
        "contact_data": [contact_data],
    }
    raw_df = pd.DataFrame(raw_data)

    expected_output = {
        "order_id": [order_id],
        "contact_address": [expected_address],
    }
    expected_df = pd.DataFrame(expected_output)

    result_df = create_orders_with_contact_address(raw_df)

    pd.testing.assert_frame_equal(result_df, expected_df)


def test_valid_address():
    """
    Verifies that valid contact data with city and postal code is correctly processed.
    """
    run_test_case(
        order_id=1,
        contact_data='[{ "city": "Chicago", "cp": "12345" }]',
        expected_address="Chicago, 12345",
    )


def test_missing_postal_code():
    """
    Verifies that missing postal code results in 'UNK00'.
    """
    run_test_case(
        order_id=2,
        contact_data='[{ "city": "New York" }]',
        expected_address="New York, UNK00",
    )


def test_missing_city():
    """
    Verifies that missing city name results in 'Unknown'.
    """
    run_test_case(
        order_id=3,
        contact_data='[{ "cp": "54321" }]',
        expected_address="Unknown, 54321",
    )


def test_invalid_structure():
    """
    Verifies that invalid JSON structure results in 'Unknown, UNK00'.
    """
    run_test_case(
        order_id=4,
        contact_data="invalid",
        expected_address="Unknown, UNK00",
    )


def test_empty_contact_data():
    """
    Verifies that empty contact_data results in 'Unknown, UNK00'.
    """
    run_test_case(
        order_id=5,
        contact_data="",
        expected_address="Unknown, UNK00",
    )


def test_null_contact_data():
    """
    Verifies that null contact_data results in 'Unknown, UNK00'.
    """
    run_test_case(
        order_id=6,
        contact_data=None,
        expected_address="Unknown, UNK00",
    )


def test_only_spaces():
    """
    Verifies that spaces in city and postal code result in placeholders.
    """
    run_test_case(
        order_id=7,
        contact_data='[{ "city": "   ", "cp": "   " }]',
        expected_address="Unknown, UNK00",
    )


def test_multiple_entries_in_list():
    """
    Verifies that only the first entry in the contact_data list is used.
    """
    run_test_case(
        order_id=8,
        contact_data='[{ "city": "Paris", "cp": "75001" }, { "city": "Lyon", "cp": "69000" }]',
        expected_address="Paris, 75001",
    )


def test_non_ascii_characters():
    """
    Verifies that contact_data with non-ASCII characters is processed correctly.
    """
    run_test_case(
        order_id=9,
        contact_data='[{ "city": "北京市", "cp": "100000" }]',
        expected_address="北京市, 100000",
    )


def test_completely_empty_json():
    """
    Verifies that an empty JSON results in placeholders.
    """
    run_test_case(
        order_id=10,
        contact_data='[{}]',
        expected_address="Unknown, UNK00",
    )

def test_city_is_number():
    """
    Verifies that a numeric city is replaced with 'Unknown'.
    """
    run_test_case(
        order_id=13,
        contact_data='[{ "city": "12345", "cp": "4567" }]',
        expected_address="Unknown, 4567",
    )


def test_postal_code_is_word():
    """
    Verifies that a non-alphanumeric postal code is replaced with 'UNK00'.
    """
    run_test_case(
        order_id=14,
        contact_data='[{ "city": "Chicago", "cp": "word" }]',
        expected_address="Chicago, UNK00",
    )


def test_both_invalid():
    """
    Verifies that both city and postal_code being invalid returns default values.
    """
    run_test_case(
        order_id=15,
        contact_data='[{ "city": "12345", "cp": "word" }]',
        expected_address="Unknown, UNK00",
    )


def test_valid_city_and_postal_code():
    """
    Verifies that valid city and postal code are processed correctly.
    """
    run_test_case(
        order_id=16,
        contact_data='[{ "city": "Olivos", "cp": "1234" }]',
        expected_address="Olivos, 1234",
    )


def test_postal_code_with_special_characters():
    """
    Verifies that a postal code with special characters is replaced with 'UNK00'.
    """
    run_test_case(
        order_id=17,
        contact_data='[{ "city": "Chicago", "cp": "12@34" }]',
        expected_address="Chicago, UNK00",
    )

def test_postal_code_is_numeric():
    """
    Verifies that a numeric postal code is processed correctly.
    """
    run_test_case(
        order_id=18,
        contact_data='[{ "city": "Barcelona", "cp": "08001" }]',
        expected_address="Barcelona, 08001",
    )


def test_postal_code_with_text_and_numbers():
    """
    Verifies that a postal code with text and numbers is valid'.
    """
    run_test_case(
        order_id=19,
        contact_data='[{ "city": "Madrid", "cp": "AB123" }]',
        expected_address="Madrid, AB123",
    )
