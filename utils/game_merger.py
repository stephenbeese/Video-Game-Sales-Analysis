# Imports
import pandas as pd
import numpy as np


def join_unique(s: pd.Series) -> str:
    vals = s.dropna().astype(str).unique().tolist()
    return ", ".join(sorted(vals)) if vals else np.nan


def mode_or_first(s: pd.Series):
    s = s.dropna()
    if s.empty:
        return np.nan
    m = s.mode()
    return m.iat[0] if not m.empty else s.iat[0]


def wmean(values: pd.Series, weights: pd.Series):
    v = values.copy()
    w = weights.copy()
    mask = v.notna() & w.notna() & (w > 0)
    if not mask.any():
        return np.nan
    return np.average(v[mask], weights=w[mask])


# def should_merge(
#     group: pd.DataFrame,
#     max_year_span: int = 1,
#     max_critic_diff: float = 5.0,
#     require_same_publisher: bool = False,
# ) -> bool:
#     """
#     Decide if rows for the same Name should be merged across platforms/years.
#     """
#     year_span = group["Year_of_Release"].max() - group["Year_of_Release"].min()
#     cs = group["Critic_Score"].dropna()
#     critic_range = (cs.max() - cs.min()) if not cs.empty else 0.0

#     if require_same_publisher and group["Publisher"].dropna().nunique() > 1:
#         return False

#     return (year_span <= max_year_span) and (critic_range <= max_critic_diff)


def should_merge(
    group, max_year_span=5, max_critic_diff=5.0, require_same_publisher=False
):
    # ----- year span -----
    year_span = 0
    if "Year_of_Release" in group.columns:
        yrs = pd.to_numeric(
            group["Year_of_Release"].replace("Unknown", np.nan), errors="coerce"
        )
        yrs = yrs[yrs >= 0].dropna()
        if not yrs.empty:
            year_span = int(yrs.max() - yrs.min())
    # Guard against NA
    if pd.isna(year_span):
        year_span = 0

    # ----- critic range -----
    critic_range = 0.0
    if "Critic_Score" in group.columns:
        cs = pd.to_numeric(group["Critic_Score"], errors="coerce").dropna()
        if not cs.empty:
            critic_range = float(cs.max() - cs.min())
    if pd.isna(critic_range):
        critic_range = 0.0

    # ----- same publisher check (optional) -----
    if require_same_publisher and "Publisher" in group.columns:
        if group["Publisher"].dropna().nunique() > 1:
            return False

    # Final boolean with plain Python numbers
    return (float(year_span) <= float(max_year_span)) and (
        float(critic_range) <= float(max_critic_diff)
    )


def aggregate_block(block: pd.DataFrame) -> dict:
    """Aggregate sales, counts, weighted scores, and pick representative metadata."""
    return {
        "Name": block["Name"].iloc[0],
        "Year_of_Release": block["Year_of_Release"].min(),
        "Platform": join_unique(block["Platform"]),
        "Genre": mode_or_first(block["Genre"]),
        "Publisher": mode_or_first(block["Publisher"]),
        "Developer": mode_or_first(block["Developer"]),
        "Rating": mode_or_first(block["Rating"]),
        "NA_Sales": block["NA_Sales"].sum(),
        "EU_Sales": block["EU_Sales"].sum(),
        "JP_Sales": block["JP_Sales"].sum(),
        "Other_Sales": block["Other_Sales"].sum(),
        "Global_Sales": block["Global_Sales"].sum(),
        "Critic_Count": block["Critic_Count"].sum(),
        "User_Count": block["User_Count"].sum(),
        "Critic_Score": wmean(block["Critic_Score"], block["Critic_Count"]),
        "User_Score": wmean(block["User_Score"], block["User_Count"]),
    }


def build_merged_df(
    df: pd.DataFrame, max_year_span=1, max_critic_diff=5.0, require_same_publisher=False
) -> pd.DataFrame:
    """
    Build the merged dataframe using the rules defined above.
    """
    rows = []
    for name, name_grp in df.groupby("Name"):
        if should_merge(
            name_grp,
            max_year_span=max_year_span,
            max_critic_diff=max_critic_diff,
            require_same_publisher=require_same_publisher,
        ):
            rows.append(aggregate_block(name_grp))
        else:
            for _, sub in name_grp.groupby("Year_of_Release"):
                rows.append(aggregate_block(sub))
    return (
        pd.DataFrame(rows)
        .sort_values("Global_Sales", ascending=False)
        .reset_index(drop=True)
    )
