import pandas as pd
from pprint import pprint


def get_dataframe_info(df):
    """
    Get a summary of the dataframe including dtypes and memory usage.
    """
    df_info = pd.DataFrame(
        [
            {
                "rows": df.shape[0],
                "columns": df.shape[1],
                "column_names": df.columns.tolist(),
                "missing_values_per_column": df.isna().sum().to_dict(),
                "duplicate_rows": df.duplicated().sum(),
                "data_types": df.dtypes.astype(str).to_dict(),
            }
        ]
    )

    # return df_info
    pprint(df_info)
