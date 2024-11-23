from src.task_4.task_4_comissions import *
from src.task_4.load_data import *
from tests.utils import locate_test_file
import pytest
import psycopg2
import pandas as pd

HOST = "localhost"

# Session scope is at the beggining of the execution
@pytest.fixture(scope='session')
def db_connection():
    print("hello")
    conn = psycopg2.connect(
        dbname="data_engineering_test",
        user="user",
        password="password",
        host=HOST,
        port="5432"
    )
    yield conn
    conn.close()

# Function scope is between each test
@pytest.fixture(scope='function')
def setup_dbt_database(db_connection):
    cursor = db_connection.cursor()
    # Clean tables before each test
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM invoicing_data;")
    db_connection.commit()

    cursor.execute("""
        INSERT INTO orders(order_id, date, company_id, company_name, crate_type, contact_data, salesowners) VALUES
            ('f47ac10b-58cc-4372-a567-0e02b2c3d479', '2023-11-10', '1e2b47e6-499e-41c6-91d3-09d12dddfbbd', 'Company A', 'Type1', '[{"phone": "1234"}]', 'Alice, Bob'),
            ('f47ac10b-58cc-4372-a567-0e02b2c3d480', '2023-11-11', '0f05a8f1-2bdf-4be7-8c82-4c9b58f04898', 'Company B', 'Type2', '[{"phone": "5678"}]', 'Alice, Charlie'),
            ('f47ac10b-58cc-4372-a567-0e02b2c3d481', '2023-11-12', '1e2b47e6-499e-41c6-91d3-09d12dddfbbd', 'Company C', 'Type3', '[{"phone": "9101"}]', 'Nicholas, Michael, Nathaniel'),
            ('f47ac10b-58cc-4372-a567-0e02b2c3d482', '2023-11-13', '1c4b0b50-1d5d-463a-b56e-1a6fd3aeb7d6', 'Company D', 'Type4', '[{"phone": "1122"}]', 'Valentina, Max, Stuart, John');
    """)
    cursor.execute("""
        INSERT INTO invoicing_data(id, order_id, company_id, gross_value, vat) VALUES
            ('e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1', 'f47ac10b-58cc-4372-a567-0e02b2c3d479', '1e2b47e6-499e-41c6-91d3-09d12dddfbbd', 20000, 20),
            ('e2e2e2e2-e2e2-e2e2-e2e2-e2e2e2e2e2e2', 'f47ac10b-58cc-4372-a567-0e02b2c3d480', '0f05a8f1-2bdf-4be7-8c82-4c9b58f04898', 15000, 10),
            ('e3e3e3e3-e3e3-e3e3-e3e3-e3e3e3e3e3e3', 'f47ac10b-58cc-4372-a567-0e02b2c3d481', '1e2b47e6-499e-41c6-91d3-09d12dddfbbd', 25000, 15),
            ('e4e4e4e4-e4e4-e4e4-e4e4-e4e4e4e4e4e4', 'f47ac10b-58cc-4372-a567-0e02b2c3d482', '1c4b0b50-1d5d-463a-b56e-1a6fd3aeb7d6', 30000, 18);
    """)
    db_connection.commit()

    yield cursor
    # Cleans tables after each test
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM invoicing_data;")
    db_connection.commit()
    cursor.close()

# Function scope is between each test
@pytest.fixture(scope='function')
def setup_database(db_connection):
    cursor = db_connection.cursor()
    # Clean tables before each test
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM invoicing_data;")
    db_connection.commit()
    yield cursor
    # Cleans tables after each test
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM invoicing_data;")
    db_connection.commit()
    cursor.close()

def get_locate_test_paths(orders_file, invoicing_file):
    return [locate_test_file(orders_file), locate_test_file(invoicing_file)]

def test_convert_date_valid():
    """
    Verifies that the function transforms correctly the date from 'DD.MM.YY' to 'YYYY-MM-DD'.
    """
    input_date = "25.12.23"
    expected_output = "2023-12-25"
    
    assert convert_date(input_date) == expected_output

def test_clean_contact_data_valid():
    """
    Ensures that clean_contact_data returns the input value unchanged for valid non-empty input.
    """
    input_value = '{"contact_name":"Curtis"}'
    expected_output = '{"contact_name":"Curtis"}'
    assert clean_contact_data(input_value) == expected_output

def test_clean_contact_data_null_input():
    """
    Ensures that clean_contact_data returns an empty string if the input is None.
    """
    input_value = None
    expected_output = ""
    assert clean_contact_data(input_value) == expected_output

def test_clean_contact_data_empty_string():
    """
    Ensures that clean_contact_data returns an empty string for an empty input.
    """
    input_value = ""
    expected_output = ""
    assert clean_contact_data(input_value) == expected_output

def test_clean_contact_data_nan():
    """
    Ensures that clean_contact_data returns an empty string if the input is NaN (pd.NA).
    """
    input_value = None
    expected_output = ""
    assert clean_contact_data(input_value) == expected_output

def test_load_data_to_postgres_valid_files(setup_database):
    """
    Ensures that load_data_to_postgres successfully loads valid orders and invoicing data.
    """
    # Override the file paths, because in the load_data I'm already using these global constants to load the files directly.
    test_paths = get_locate_test_paths("sample.csv", "sample.json")
    load_data_to_postgres(HOST, test_paths)

    # We verify the orders table and see if it has records
    setup_database.execute("SELECT * FROM orders;")
    orders_results = setup_database.fetchall()
    assert len(orders_results) > 0  # Ensure records were inserted

    # Same with invoicing
    setup_database.execute("SELECT * FROM invoicing_data;")
    invoicing_results = setup_database.fetchall()
    assert len(invoicing_results) > 0

def test_load_data_to_postgres_empty_files():
    """
    Ensures that load_data_to_postgres handles an empty orders.csv file.
    """
    test_paths = get_locate_test_paths("empty_sample.csv", "empty_sample.json")

    with pytest.raises(Exception) as excinfo:
        load_data_to_postgres(HOST, test_paths)

    # Assert the exception message
    assert "orders.csv is empty." in str(excinfo.value)

def test_load_data_to_postgres_missing_columns_files():
    """
    Ensures that load_data_to_postgres handles files with missing columns gracefully.
    """
    test_paths = get_locate_test_paths("missing_columns_sample.csv", "missing_columns_sample.json")

    with pytest.raises(Exception) as excinfo:
        load_data_to_postgres(HOST, test_paths)

    # Assert the exception message
    assert "orders.csv is empty" in str(excinfo.value)

def test_load_data_to_postgres_file_not_found():
    """
    Ensures that load_data_to_postgres raises an error when a required file is missing.
    """
    # Provide non-existent file paths
    test_paths = get_locate_test_paths("non_existent_orders.csv", "non_existent_invoicing.json")


    with pytest.raises(FileNotFoundError) as excinfo:
        load_data_to_postgres(HOST, test_paths)

    # Assert that the exception mentions the missing file
    assert "Orders file not found" in str(excinfo.value) or "Invoicing file not found" in str(excinfo.value)

def test_load_data_to_postgres_missing_keys_json():
    """
    Ensures that load_data_to_postgres handles JSON files with missing keys gracefully.
    """
    test_paths = get_locate_test_paths("sample.csv", "missing_columns_sample.json")  # missing_keys_sample.json must lack required keys like "id"

    with pytest.raises(Exception) as excinfo:
        load_data_to_postgres(HOST, test_paths)

    assert "Missing required key" in str(excinfo.value)

def test_dbt_view_results(setup_dbt_database):
    """
    Ensures that the view generated by DBT `calculate_comissions` returns the correct results.
    """
    run_dbt()

    df = fetch_dbt_results(HOST, view_name=VIEW_NAME)

    expected_data = {
        'salesowner': ['Alice', 'Valentina', 'Nicholas', 'Max', 'Michael', 'Bob', 'Charlie', 'Stuart', 'Nathaniel', 'John'],
        'total_commission': [18.18, 15.25, 13.04, 6.36, 5.43, 4.17, 3.41, 2.42, 2.07, 0.0]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(
        df.sort_values(by="salesowner").reset_index(drop=True),
        expected_df.sort_values(by="salesowner").reset_index(drop=True),
        check_dtype=False
    )

