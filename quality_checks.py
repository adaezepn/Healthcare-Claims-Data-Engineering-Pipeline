import pandas as pd


def check_duplicates(df, primary_key):
    """Check for duplicate primary keys."""
    duplicates = df.duplicated(subset=[primary_key]).sum()

    return {
        "check": "Duplicate Primary Keys",
        "status": "PASS" if duplicates == 0 else "FAIL",
        "count": int(duplicates)
    }


def check_missing_values(df):
    """Return missing values for every column."""
    missing = df.isnull().sum()

    return {
        "check": "Missing Values",
        "results": missing.to_dict()
    }


def check_data_types(df):
    """Return data types."""
    return {
        "check": "Data Types",
        "results": df.dtypes.astype(str).to_dict()
    }


def check_negative_values(df, exclude_columns=None):
    """Find negative values in numeric columns, excluding columns where negatives are valid."""
    if exclude_columns is None:
        exclude_columns = []

    results = {}
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        if col in exclude_columns:
            continue

        negative_count = (df[col] < 0).sum()

        if negative_count > 0:
            results[col] = int(negative_count)

    return {
        "check": "Negative Values",
        "results": results
    }


def check_allowed_values(df, column, allowed_values, ignore_nulls=True):
    """Validate categorical values."""
    series = df[column]

    if ignore_nulls:
        series = series.dropna()

    invalid = series.loc[~series.isin(allowed_values)]

    return {
        "check": f"Allowed Values ({column})",
        "status": "PASS" if len(invalid) == 0 else "FAIL",
        "invalid_count": int(len(invalid)),
        "invalid_values": invalid.unique().tolist()
    }