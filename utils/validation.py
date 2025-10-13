"""
Utility functions for statistical validation tests.
"""

from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def run_anova_by_region(df, regions, vendors):
    """
    Runs one-way ANOVA tests for each region across vendors.

    Parameters:
    - df (pd.DataFrame): Cleaned dataset containing sales columns (e.g. 'JP_Sales', 'NA_Sales').
    - regions (list): List of region column names to test, e.g. ['JP_Sales', 'NA_Sales'].
    - vendors (list): List of vendors to compare (default = Nintendo, Sony, Microsoft, Other).

    Returns:
        dict: Dictionary with region names as keys and ANOVA results as values.
    """

    results = {}
    for region in regions:
        samples = [df[df["Vendor"] == v][region] for v in vendors]
        anova_result = f_oneway(*samples)
        results[region] = anova_result

        print(
            f"ANOVA ({region.replace(
                '_Sales', '')}): F = {anova_result.statistic:.3f}, p = {anova_result.pvalue:.5f}"
        )

    return results


def run_tukey_by_region(df, regions, print_results=True):
    """
    Runs Tukey's HSD post-hoc tests for each region to identify
    which vendor sales differ significantly.

    Parameters:
        df (pd.DataFrame): Dataset with vendor and sales columns.
        regions (list): List of region column names (e.g. ['JP_Sales', 'NA_Sales', 'EU_Sales']).
        vendors (list): List of vendor names (default = Nintendo, Sony, Microsoft, Other).
    """

    for region in regions:
        data = df[["Vendor", region]].dropna()

        tukey = pairwise_tukeyhsd(endog=data[region], groups=data["Vendor"], alpha=0.05)
        if print_results:
            print(f"\n Tukey HSD Results for {region.replace('_Sales', '')}:")
            print(tukey.summary())
