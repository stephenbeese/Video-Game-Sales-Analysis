def convert_dtypes(df):
    """
    Convert dataframe columns to appropriate dtypes for memory efficiency and analysis.
    """
    # Convert Year_of_Release to nullable int
    df["Year_of_Release"] = df["Year_of_Release"].astype("Int64")

    # Optionally convert Critic_Score to int if you want
    df["Critic_Score"] = df["Critic_Score"].astype("Int64")

    # Convert categorical columns
    cat_cols = ["Platform", "Genre", "Publisher", "Developer", "Rating"]
    df[cat_cols] = df[cat_cols].astype("category")

    return df


def clean_data(df):
    # Remove rows where 'Name' or 'Global_Sales' is unknown
    df.dropna(subset=["Name", "Global_Sales"], inplace=True)

    # Replace missing publishers with 'Unknown'
    df["Publisher"] = df["Publisher"].fillna("Unknown")

    # Add 'Unknown' to the categories first (if Developer is categorical)
    df["Developer"] = df["Developer"].cat.add_categories("Unknown")

    # Fill missing Developer with 'Unknown'
    df["Developer"] = df["Developer"].fillna("Unknown")

    # Drop columns that are not needed for analysis
    df.drop(
        columns=["Critic_Score", "Critic_Count", "User_Score", "User_Count", "Rating"],
        inplace=True,
    )

    # Fill missing Year_of_Release with -1 and convert to Int64
    df["Year_of_Release"] = df["Year_of_Release"].fillna(-1).astype("Int64")

    return df


def remove_review_cols(df):
    """
    Remove review-related columns from the dataframe.
    """
    review_cols = [
        "Critic_Score",
        "Critic_Count",
        "User_Score",
        "User_Count",
        "Rating",
    ]
    return df.drop(columns=review_cols, errors="ignore")
