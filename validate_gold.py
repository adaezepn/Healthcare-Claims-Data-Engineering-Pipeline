from pathlib import Path
import pandas as pd

project_folder = Path(__file__).parent
gold_file = project_folder / "gold" / "healthcare_claims_analytics.csv"

df = pd.read_csv(gold_file)

print("Gold Dataset Validation")
print("=" * 50)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nDuplicate CLAIM_IDs:")
print(df.duplicated(subset=["CLAIM_ID"]).sum())

key_columns = [
    "CLAIM_ID",
    "PATIENT_ID",
    "PROVIDER_ID",
    "ENCOUNTER_ID",
    "AGE",
    "GENDER",
    "PRIMARY_PATIENT_INSURANCE_ID",
]

print("\nMissing values in key columns:")
print(df[key_columns].isnull().sum())

print("\nSample rows:")
print(df.head())

print("\nValidation complete.")