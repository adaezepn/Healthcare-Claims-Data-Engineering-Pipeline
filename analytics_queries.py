import pandas as pd
from pathlib import Path

GOLD_FILE = Path("gold/healthcare_claims_analytics.csv")
REPORT_FILE = Path("reports/analytics_report.txt")

REPORT_FILE.parent.mkdir(exist_ok=True)

gold = pd.read_csv(GOLD_FILE)

with open(REPORT_FILE, "w", encoding="utf-8") as report:
    report.write("Healthcare Claims Analytics Report\n")
    report.write("=" * 45 + "\n\n")

    report.write(f"Total Rows: {len(gold)}\n")
    report.write(f"Total Columns: {len(gold.columns)}\n\n")

    report.write("Columns Available:\n")
    report.write(", ".join(gold.columns) + "\n\n")

    # Top 10 most expensive claims
    if "CLAIM_COST" in gold.columns:
        report.write("Top 10 Most Expensive Claims\n")
        report.write("-" * 35 + "\n")
        report.write(
            gold.nlargest(10, "CLAIM_COST").to_string(index=False)
        )
        report.write("\n\n")

        report.write("Average Claim Cost\n")
        report.write("-" * 35 + "\n")
        report.write(f"${gold['CLAIM_COST'].mean():,.2f}\n\n")

    # Claims by payer
    if "PAYER_NAME" in gold.columns and "CLAIM_ID" in gold.columns:
        report.write("Claims by Payer\n")
        report.write("-" * 35 + "\n")
        report.write(
            gold.groupby("PAYER_NAME")["CLAIM_ID"]
            .count()
            .sort_values(ascending=False)
            .to_string()
        )
        report.write("\n\n")

    # Claims by gender
    if "GENDER" in gold.columns and "CLAIM_ID" in gold.columns:
        report.write("Claims by Gender\n")
        report.write("-" * 35 + "\n")
        report.write(
            gold.groupby("GENDER", dropna=False)["CLAIM_ID"]
            .count()
            .sort_values(ascending=False)
            .to_string()
        )
        report.write("\n\n")

    # Average age
    if "AGE" in gold.columns:
        report.write("Average Patient Age\n")
        report.write("-" * 35 + "\n")
        report.write(f"{gold['AGE'].mean():.2f}\n\n")

    # Top providers
    if "PROVIDER_NAME" in gold.columns and "CLAIM_ID" in gold.columns:
        report.write("Top Providers by Claim Count\n")
        report.write("-" * 35 + "\n")
        report.write(
            gold.groupby("PROVIDER_NAME")["CLAIM_ID"]
            .count()
            .sort_values(ascending=False)
            .head(10)
            .to_string()
        )
        report.write("\n\n")

    # Claim status distribution
    if "CLAIM_STATUS" in gold.columns:
        report.write("Claim Status Distribution\n")
        report.write("-" * 35 + "\n")
        report.write(
            gold["CLAIM_STATUS"]
            .value_counts(dropna=False)
            .to_string()
        )
        report.write("\n\n")

    # Encounter type distribution
    if "ENCOUNTER_TYPE" in gold.columns:
        report.write("Encounter Type Distribution\n")
        report.write("-" * 35 + "\n")
        report.write(
            gold["ENCOUNTER_TYPE"]
            .value_counts(dropna=False)
            .head(10)
            .to_string()
        )
        report.write("\n\n")

    report.write("Notes\n")
    report.write("-" * 35 + "\n")
    report.write(
        "Some demographic fields may contain missing values because the original "
        "tables were sampled independently using LIMIT 1000. This affected "
        "referential integrity between claims and related patient/provider records.\n"
    )

print(f"Analytics report generated: {REPORT_FILE}")