import json
import os
import pandas as pd

from pipelines.load import create_and_load_table


def run_brfss_etl_pipeline(path: str, table_name: str) -> None:
    # Verify file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at path '{path}' does not exist.")
    
    # Fetch the column map for brfss
    with open("config/brfss_column_map.json") as f:
        brfss_column_map = json.load(f)

    # Open brfss file
    with open(path) as f:
        i = 10
        print(i)
        # Read each line
        for line in f:
            
            if i <= 0:
                break
            # Initialize the row dictionary
            row_dict = {}

            # Map the values to the columns
            for header, map in brfss_column_map.items():
                row_dict[header] = [line[map['column'] - 1 : map['column'] + map['length'] - 1]]

            # Create a DataFrame from the row dictionary
            df = pd.DataFrame(row_dict)

            # Load to database
            create_and_load_table(
                df=df,
                table_name=table_name,
                schema="raw",
                if_exists="append"
            )

            i = i-1

    print(f"Raw ETL pipeline completed for table '{table_name}'.")

if __name__ == "__main__":
    # Fetch the path and table name for the raw data
    with open("config/raw_data_map.json") as f:
        raw_data_map = json.load(f)

    # Set the data source
    source = raw_data_map['brfss']

    try:
        # Run the pipeline
        run_brfss_etl_pipeline(path=source['path'], table_name=source['table_name'])

    except Exception as e:
        raise RuntimeError(f"Error during brfss ETL pipeline: {e}")