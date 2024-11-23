import pandas as pd
import matplotlib.pyplot as plt
from src.utils import getFilepath

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

    # Replace the null values in company_name with "Unknown" to include orders without an associated company in the analysis.
    # I'm assuming here that we should still keep track of the crates that don't have a company name associated.
    raw_dataframe["company_name"] = raw_dataframe["company_name"].fillna("Unknown")

    # Another assumption here, if a crate type is set to null it will count as an "Unknown Crate"
    raw_dataframe["crate_type"] = raw_dataframe["crate_type"].fillna("Unknown Crate")

    # another assumption as well, There can't be two order ids 
    raw_dataframe = raw_dataframe.drop_duplicates(subset="order_id")

    distribution = (
        raw_dataframe.groupby(["company_name", "crate_type"]) 
        .size()  # Aggregate function to count how many combinations of the group by we have.
        .unstack(fill_value=0)  # Unstack the crate type to have a better format, we also fill nulls with 0.
    )

    # At least these columns should show in the final dataframe.
    required_crate_types = ["Metal", "Plastic", "Wood"]

    # Ensure all required crate types are present
    for crate in required_crate_types:
        if crate not in distribution.columns:
            distribution[crate] = 0  # Add missing required crate type with all zeros

    # Here I'm making another assumption: if the crate types are null for a company, 
    # instead of dropping the whole record, the company should still show with zero value for all the crate types.
    # Additionally, I'm assuming there could be more than three types of crate (like Fiberglass for example)
    # So I'm sorting the final columns for testing.
    crate_types = sorted(distribution.columns.dropna().unique())

    # We order the columns in the expected order
    distribution = distribution[crate_types]

    return distribution

def bar_plot_df(distribution_df):
    """
    Creates and shows a Bar plot with the count of orders per crater type per company.

    Args:
        distribution_df: pd.DataFrame type previously processed.
    
    Returns:
        None
    """
    distribution_df.plot(kind="bar", figsize=(10, 6))
    plt.title("Distribution of Crate Types per Company")
    plt.ylabel("Number of Orders")
    plt.xlabel("Company Name")
    plt.legend(title="Crate Type")
    plt.tight_layout()
    plt.show()

def main():
    orders_filepath = getFilepath("orders.csv")
    orders_df = load_csv_to_dataframe(orders_filepath)
    distribution_df = calculate_crate_distribution(orders_df)
    print(distribution_df)
    bar_plot_df(distribution_df)

if __name__ == '__main__':
    main()