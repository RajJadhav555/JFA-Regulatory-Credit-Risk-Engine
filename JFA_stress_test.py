import pandas as pd
import numpy as np

df = pd.read_csv("underwritten_portfolio.csv")

#Define Macroeconomic Rate Shock (+300 bps = +3.0%)

RATE_SHOCK = 3.0
stressed_monthly_rate = (df["Rate"] + RATE_SHOCK) / (12 * 100)
total_months = df["Tenure_Years"] *12

#Compute Stressed EMI and Stressed FOIR

df["Stressed_EMI"] = round(
    df["Principal"] * stressed_monthly_rate * ((1 + stressed_monthly_rate) ** total_months) /
    (((1 + stressed_monthly_rate) ** total_months) -1), 2
)
df["Stressed_FOIR_%"] = round((df["Stressed_EMI"] / df["Monthly_Income"]) * 100, 2)
cols_to_view = ["Name", "Decision", "Monthly_EMI", "Stressed_EMI", "FOIR_%", "Stressed_FOIR_%"]
print(df[cols_to_view])

#Stress Testing Classification

is_approved = df["Decision"].str.contains("APPROVED")

conditions = [
    is_approved & (df["Stressed_FOIR_%"] > 50.0),
    is_approved & (df["Stressed_FOIR_%"] <= 50.0),
]
choices = ["VULNERABLE: Breached 50%", "RESILIENT: Absorbed shock"]

df["Stressed_Status"] = np.select(conditions, choices, default="UNAFFECTED: Baseline Rejection")

#Calculate shock Deltas

df["EMI_Shock_Delta"] = round(df["Stressed_EMI"] - df["Monthly_EMI"],2)
df["FOIR_Shock_Delta"] = round(df["Stressed_FOIR_%"] - df["FOIR_%"],2)
print("\n================== MACROECONOMIC STRESS TEST REPORT (+300 BPS) ==================")
print(df[["Name", "Stressed_Status", "Monthly_EMI", "Stressed_EMI", "EMI_Shock_Delta", "Stressed_FOIR_%"]])

#Export Stress Portfolio Governace Report 
df.to_csv("stressed_portfolio_report.csv", index = False)
print("\n[SUCCESS] Stressed portfolio report exported to stressed_portfolio_report.csv")
