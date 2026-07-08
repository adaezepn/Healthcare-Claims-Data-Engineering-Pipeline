from pathlib import Path
import pandas as pd

project_folder = Path(__file__).parent
silver_folder = project_folder / "silver"
gold_folder = project_folder / "gold"
gold_folder.mkdir(exist_ok=True)

claims = pd.read_csv(silver_folder / "claims_silver.csv")
patients = pd.read_csv(silver_folder / "patients_silver.csv")
providers = pd.read_csv(silver_folder / "providers_silver.csv")
payers = pd.read_csv(silver_folder / "payers_silver.csv")
encounters = pd.read_csv(silver_folder / "encounters_silver.csv")

# Join claims to patients
gold = claims.merge(
    patients,
    on="PATIENT_ID",
    how="left",
    suffixes=("", "_PATIENT")
)

# Join providers
gold = gold.merge(
    providers,
    on="PROVIDER_ID",
    how="left",
    suffixes=("", "_PROVIDER")
)

# Join encounters
gold = gold.merge(
    encounters,
    on="ENCOUNTER_ID",
    how="left",
    suffixes=("", "_ENCOUNTER")
)

# Join payers
gold = gold.merge(
    payers,
    left_on="PRIMARY_PATIENT_INSURANCE_ID",
    right_on="PAYER_ID",
    how="left",
    suffixes=("", "_PAYER")
)

# Save Gold CSV
gold_csv = gold_folder / "healthcare_claims_analytics.csv"
gold.to_csv(gold_csv, index=False)

# Save Gold Parquet
gold_parquet = gold_folder / "healthcare_claims_analytics.parquet"
gold.to_parquet(gold_parquet, index=False)

print("Gold dataset created successfully.")
print(f"Rows: {gold.shape[0]}")
print(f"Columns: {gold.shape[1]}")
print(f"CSV: {gold_csv}")
print(f"Parquet: {gold_parquet}")