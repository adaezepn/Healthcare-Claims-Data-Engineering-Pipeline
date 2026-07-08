import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

load_dotenv()

mfa_code = input("Enter MFA code: ")

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    passcode=mfa_code
)

tables = {
    "patients": """
        SELECT
            PATIENT_ID, BIRTHDATE, DEATHDATE, MARITAL, RACE, ETHNICITY,
            GENDER, CITY, STATE, COUNTY, ZIP, HEALTHCARE_EXPENSES,
            HEALTHCARE_COVERAGE, INCOME
        FROM SYNTHETIC_HEALTHCARE_DATA__CLINICAL_AND_CLAIMS.SILVER.PATIENTS
        LIMIT 1000
    """,
    "providers": """
        SELECT
            PROVIDER_ID, ORGANIZATION_ID, GENDER, SPECIALITY,
            CITY, STATE, ZIP, ENCOUNTERS, PROCEDURES
        FROM SYNTHETIC_HEALTHCARE_DATA__CLINICAL_AND_CLAIMS.SILVER.PROVIDERS
        LIMIT 1000
    """,
    "payers": """
        SELECT
            PAYER_ID, NAME, CITY, STATE_HEADQUARTERED, AMOUNT_COVERED,
            AMOUNT_UNCOVERED, REVENUE, COVERED_ENCOUNTERS,
            UNCOVERED_ENCOUNTERS, UNIQUE_CUSTOMERS, MEMBER_MONTHS
        FROM SYNTHETIC_HEALTHCARE_DATA__CLINICAL_AND_CLAIMS.SILVER.PAYERS
    """,
    "encounters": """
        SELECT
            ENCOUNTER_ID, ENCOUNTER_START, ENCOUNTER_STOP, PATIENT_ID,
            ORGANIZATION_ID, PROVIDER_ID, PAYER_ID, ENCOUNTERCLASS,
            CODE, DESCRIPTION, BASE_ENCOUNTER_COST, TOTAL_CLAIM_COST,
            PAYER_COVERAGE, REASONCODE, REASONDESCRIPTION
        FROM SYNTHETIC_HEALTHCARE_DATA__CLINICAL_AND_CLAIMS.SILVER.ENCOUNTERS
        LIMIT 1000
    """
}

for table_name, query in tables.items():
    print(f"Extracting {table_name}...")

    df = pd.read_sql(query, conn)
    output_file = f"{table_name}_sample.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved {output_file} with {df.shape[0]} rows and {df.shape[1]} columns")

conn.close()

print("All core tables extracted successfully.")