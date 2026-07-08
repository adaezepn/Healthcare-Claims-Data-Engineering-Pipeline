from pathlib import Path
import pandas as pd

project_folder = Path(__file__).parent
silver_folder = project_folder / "silver"
silver_folder.mkdir(exist_ok=True)

# ---------- PATIENTS ----------
patients = pd.read_csv(project_folder / "patients_raw_sample.csv")

patients["BIRTHDATE"] = pd.to_datetime(patients["BIRTHDATE"], errors="coerce")
patients["DEATHDATE"] = pd.to_datetime(patients["DEATHDATE"], errors="coerce")

today = pd.Timestamp.today()
patients["AGE"] = ((today - patients["BIRTHDATE"]).dt.days / 365.25)
patients["AGE"] = pd.to_numeric(patients["AGE"], errors="coerce").round().astype("Int64")

patients_silver = patients[
    [
        "PATIENT_ID",
        "AGE",
        "DEATHDATE",
        "MARITAL",
        "RACE",
        "ETHNICITY",
        "GENDER",
        "CITY",
        "STATE",
        "COUNTY",
        "ZIP",
        "HEALTHCARE_EXPENSES",
        "HEALTHCARE_COVERAGE",
        "INCOME",
        "SYNTHEA_CITY",
    ]
]

patients_silver.to_csv(silver_folder / "patients_silver.csv", index=False)


# ---------- CLAIMS ----------
claims = pd.read_csv(project_folder / "claims_raw_sample.csv")

date_cols = [
    "CURRENTILLNESSDATE",
    "SERVICEDATE",
    "LASTBILLEDDATE1",
    "LASTBILLEDDATE2",
    "LASTBILLEDDATEP",
]

for col in date_cols:
    claims[col] = pd.to_datetime(claims[col], errors="coerce")

claims_silver = claims[
    [
        "CLAIM_ID",
        "PATIENT_ID",
        "PROVIDER_ID",
        "PRIMARY_PATIENT_INSURANCE_ID",
        "SECONDARY_PATIENT_INSURANCE_ID",
        "ENCOUNTER_ID",
        "SERVICEDATE",
        "STATUS1",
        "STATUS2",
        "STATUSP",
        "OUTSTANDING1",
        "OUTSTANDING2",
        "OUTSTANDINGP",
        "HEALTHCARECLAIMTYPEID1",
        "HEALTHCARECLAIMTYPEID2",
        "SYNTHEA_CITY",
    ]
]

claims_silver.to_csv(silver_folder / "claims_silver.csv", index=False)


# ---------- PROVIDERS ----------
providers = pd.read_csv(project_folder / "providers_raw_sample.csv")

providers_silver = providers[
    [
        "PROVIDER_ID",
        "ORGANIZATION_ID",
        "GENDER",
        "SPECIALITY",
        "CITY",
        "STATE",
        "ZIP",
        "ENCOUNTERS",
        "PROCEDURES",
        "SYNTHEA_CITY",
    ]
]

providers_silver.to_csv(silver_folder / "providers_silver.csv", index=False)


# ---------- PAYERS ----------
payers = pd.read_csv(project_folder / "payers_raw_sample.csv")

payers_silver = payers[
    [
        "PAYER_ID",
        "NAME",
        "AMOUNT_COVERED",
        "AMOUNT_UNCOVERED",
        "REVENUE",
        "COVERED_ENCOUNTERS",
        "UNCOVERED_ENCOUNTERS",
        "UNIQUE_CUSTOMERS",
        "QOLS_AVG",
        "MEMBER_MONTHS",
        "SYNTHEA_CITY",
    ]
]

payers_silver.to_csv(silver_folder / "payers_silver.csv", index=False)


# ---------- ENCOUNTERS ----------
encounters = pd.read_csv(project_folder / "encounters_raw_sample.csv")

encounters["ENCOUNTER_START"] = pd.to_datetime(encounters["ENCOUNTER_START"], errors="coerce")
encounters["ENCOUNTER_STOP"] = pd.to_datetime(encounters["ENCOUNTER_STOP"], errors="coerce")

encounters_silver = encounters[
    [
        "ENCOUNTER_ID",
        "ENCOUNTER_START",
        "ENCOUNTER_STOP",
        "PATIENT_ID",
        "ORGANIZATION_ID",
        "PROVIDER_ID",
        "PAYER_ID",
        "ENCOUNTERCLASS",
        "DESCRIPTION",
        "BASE_ENCOUNTER_COST",
        "TOTAL_CLAIM_COST",
        "PAYER_COVERAGE",
        "REASONDESCRIPTION",
        "SYNTHEA_CITY",
    ]
]

encounters_silver.to_csv(silver_folder / "encounters_silver.csv", index=False)

print("Silver files created successfully.")