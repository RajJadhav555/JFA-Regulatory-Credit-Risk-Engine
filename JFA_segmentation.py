import pandas as pd
import numpy as np
df = pd.read_csv("underwritten_portfolio.csv")

#Define Credit Risk Tiers based on instituitional CIBIL benchmarks

tier_conditions = [
    df["CIBIL"] >= 750,
    (df["CIBIL"] >= 650) & (df["CIBIL"] < 750),
    df["CIBIL"] < 650
]

tier_labels = ["Tier 1: Prime", "Tier 2: Near-Prime", "Tier 3: Sub-Prime"]

df["Risk_Tier"] = np.select(tier_conditions, tier_labels, default = "Unclassified")

print(df[["Applicant_ID", "Name", "CIBIL", "FOIR_%", "Risk_Tier", "Decision"]])

#Aggregate instituitional risk metrics per credit tier

tier_summary = df.groupby("Risk_Tier").agg(
    Total_Capital=("Principal","sum"),
    Avg_CIBIL=("CIBIL","mean"),
    Avg_FOIR=("FOIR_%","mean"),
    Borrower_count=("Applicant_ID","count")
).reset_index()

print("\n--- EXECUTIVE RISK GOVERNANCE TABLE ---")
print(tier_summary)

#Calculate Capital Concentrattion Share(%) and clean up rounding

total_capital=tier_summary["Total_Capital"].sum()
tier_summary["Capital_Share_%"] = (tier_summary["Total_Capital"] / total_capital * 100).round(2)
tier_summary["Avg_FOIR"] = tier_summary["Avg_FOIR"].round(2)

#Export executive report for credit committee
tier_summary.to_csv("risk_governence_summary.csv", index=False)

print("\n-- Final EXECUTIVE RISK GOVERNENCE REPORT --")
print(tier_summary.to_string(index=False))


