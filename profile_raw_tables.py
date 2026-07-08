from pathlib import Path
import pandas as pd

from quality_checks import (
    check_duplicates,
    check_missing_values,
    check_data_types,
    check_negative_values,
    check_allowed_values
)

project_folder = Path(__file__).parent
reports_folder = project_folder / "reports"
reports_folder.mkdir(exist_ok=True)

tables = {
    "CLAIMS": {
        "file": "claims_raw_sample.csv",
        "primary_key": "CLAIM_ID"
    },
    "PATIENTS": {
        "file": "patients_raw_sample.csv",
        "primary_key": "PATIENT_ID"
    },
    "PROVIDERS": {
        "file": "providers_raw_sample.csv",
        "primary_key": "PROVIDER_ID"
    },
    "PAYERS": {
        "file": "payers_raw_sample.csv",
        "primary_key": "PAYER_ID"
    },
    "ENCOUNTERS": {
        "file": "encounters_raw_sample.csv",
        "primary_key": "ENCOUNTER_ID"
    }
}

allowed_value_checks = {
    "CLAIMS": {
        "STATUS1": ["CLOSED", "BILLED"],
        "STATUS2": ["CLOSED", "BILLED"],
        "STATUSP": ["CLOSED", "BILLED"]
    },
    "PATIENTS": {
        "GENDER": ["M", "F"],
        "MARITAL": ["M", "S", "D", "W"]
    },
    "PROVIDERS": {
        "GENDER": ["M", "F"]
    }
}

report_lines = []

for table_name, config in tables.items():
    file_path = project_folder / config["file"]
    df = pd.read_csv(file_path)

    report_lines.append("=" * 70)
    report_lines.append(f"TABLE: {table_name}")
    report_lines.append("=" * 70)
    report_lines.append(f"Rows: {len(df)}")
    report_lines.append(f"Columns: {len(df.columns)}")
    report_lines.append("")

    duplicate_result = check_duplicates(df, config["primary_key"])
    report_lines.append(f"Duplicate {config['primary_key']}: {duplicate_result}")

    missing_result = check_missing_values(df)
    report_lines.append("\nMissing Values:")
    report_lines.append(str(missing_result))

    type_result = check_data_types(df)
    report_lines.append("\nData Types:")
    report_lines.append(str(type_result))

    negative_result = check_negative_values(df, exclude_columns=["LAT", "LON"])
    report_lines.append("\nNegative Values:")
    report_lines.append(str(negative_result))

    if table_name in allowed_value_checks:
        report_lines.append("\nAllowed Value Checks:")
        for column, allowed_values in allowed_value_checks[table_name].items():
            if column in df.columns:
                result = check_allowed_values(df, column, allowed_values)
                report_lines.append(str(result))

    report_lines.append("\n")

report_path = reports_folder / "data_quality_report_v2.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("\n".join(report_lines))

print(f"Data quality report created: {report_path}")