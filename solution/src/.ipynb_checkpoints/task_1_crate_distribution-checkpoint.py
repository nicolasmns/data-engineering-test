import pandas as pd
import matplotlib.pyplot as plt
import os

#########################################################################################
#   Test 1: Distribution of Crate Type per Company                                      #
#   Calculate the distribution of crate types per company (number of orders per type).  #
#########################################################################################


class InvalidSeparatorError(Exception):
    """Custom exception for invalid CSV separators."""
    pass

def load_csv_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Checks if the csv is an appropiate file before reading into a Dataframe.

    Args:
        file_path: string type of the filepath of a .csv file that uses ';' as separator.
    
    Returns:
        pd.DataFrame: Dataframe for the file.
    """
    EXPECTED_COLUMNS = ["order_id","date","company_id","company_name","crate_type","contact_data","salesowners"]

    try:
        df = pd.read_csv(file_path, sep=';')
        if len(df.columns) <= 1: # if the separator isn't the ';' symbol then it raises an exception
                raise pd.errors.ParserError("Invalid separator or malformed file")
         # Verify missing columns
        missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
        
        # Verify unexpected columns
        unexpected_columns = [col for col in df.columns if col not in EXPECTED_COLUMNS]
        if unexpected_columns:
            raise ValueError(f"Unexpected columns: {', '.join(unexpected_columns)}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} wasn't found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The file is empty or has no data to parse.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("The file has an invalid separator or is malformed.")
         

def calculate_crate_distribution(raw_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame with the count of orders per crater type per company.

    Args:
        raw_dataframe: pd.DataFrame type previously created.
    
    Returns:
        pd.DataFrame: DataFrame containing the columns company_name and the unstacked crate types with a count of each per company.
    """

    # Replace null values in company_name with "Unknown" to include orders without an associated company in the analysis.
    raw_dataframe["company_name"] = raw_dataframe["company_name"].fillna("Unknown")

     # Removes records where the crater type is null.
    filtered_df = raw_dataframe.dropna(subset=["crate_type"])

    distribution = (
        filtered_df.groupby(["company_name", "crate_type"])  # we group by 'company_name' and 'crate_type'.
        .size()  # Aggregate function to count how many combinations of the group by we have.
        .unstack(fill_value=0)  # Unstack the crate type to have a better format, we also fill nulls with 0.
    )

    # We make sure that all crate_types are present.
    crate_types = ["Metal", "Plastic", "Wood"]
    for crate in crate_types:
        if crate not in distribution.columns:
            distribution[crate] = 0  # Rellenar columnas ausentes con 0.
    
    # We order the columns in the expected order
    distribution = distribution[crate_types]

    return distribution

def bar_plot_df(distribution_df):
    distribution_df.plot(kind="bar", figsize=(10, 6))
    plt.title("Distribution of Crate Types per Company")
    plt.ylabel("Number of Orders")
    plt.xlabel("Company Name")
    plt.legend(title="Crate Type")
    plt.tight_layout()
    plt.show()

def main():
    orders_filepath = os.path.join(os.path.dirname(__file__), "./resources/sample.csv")
    orders_df = load_csv_to_dataframe(orders_filepath)
    distribution_df = calculate_crate_distribution(orders_df)
    bar_plot_df(distribution_df)

if __name__ == '__main__':
    main()