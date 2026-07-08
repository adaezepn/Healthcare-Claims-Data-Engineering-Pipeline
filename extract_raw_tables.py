import os
from pathlib import Path

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv


# Always use the folder where this script is saved
project_folder = Path(__file__).parent

# Load .env from the project folder
load_dotenv(project_folder / ".env")

mfa_code = input("Enter MFA code: ")

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    passcode=mfa_code
)

tables = [
    "CLAIMS",
    "PATIENTS",
    "PROVIDERS",
    "PAYERS",
    "ENCOUNTERS"
]

for table in tables:
    print(f"Extracting raw {table}...")

    query = f"""
    SELECT *
    FROM SYNTHETIC_HEALTHCARE_DATA__CLINICAL_AND_CLAIMS.SILVER.{table}
    LIMIT 1000
    """

    df = pd.read_sql(query, conn)

    output_file = project_folder / f"{table.lower()}_raw_sample.csv"
    df.to_csv(output_file, index=False)

    print(f"Saved {output_file.name}: {df.shape[0]} rows, {df.shape[1]} columns")

conn.close()

print("Raw extraction completed.")