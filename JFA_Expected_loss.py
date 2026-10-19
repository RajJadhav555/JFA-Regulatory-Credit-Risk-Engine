import pandas as pd
import numpy as np
df = pd.read_csv("underwritten_portfolio.csv")

#Calculate Probability of Default PD based on CIBIL
pd_conditions = [
    df["CIBIL"] >= 750,
    (df["CIBIL"] >= 700) & (df["CIBIL"] < 750),
    (df["CIBIL"] >= 650) & (df["CIBIL"] < 700)
]
pd_choices = [0.02, 0.05, 0.12]

df["PD"] = np.select(pd_conditions, pd_choices, default=0.25)

#Base II Expected Loss Core Engine (EL = PD * EAD * LSD)
LGD_RATE = 0.45
df["EAD"] = df["Principal"]
df["LGD"] = LGD_RATE

df["Expected_Loss"] = round(df["PD"] * df["EAD"] * df["LGD"], 2)
print(df[["Name", "CIBIL", "PD", "EAD", "Expected_Loss"]])

#Risk-Adjusted Dynamic Pricing Engine
BASE_COST_FUNDS = 7.0  #Bank's Cost to borrow whole sale money
TARGET_PROFIT_MARGIN = 2.0  # Bank's Requied Profit Margin

df["EL_Rate_%"] = round(df["Expected_Loss"] / df["EAD"] * 100, 2)
df["fair_risk_rate"] = round(BASE_COST_FUNDS + TARGET_PROFIT_MARGIN + df["EL_Rate_%"], 2)
df["Pricing_Delta"] = round(df["Rate"] - df["fair_risk_rate"], 2)
print("\n=== RISK-ADJUSTED PRICING AUDIT ===")
print(df[["Name", "Rate", "EL_Rate_%", "fair_risk_rate", "Pricing_Delta"]])

#Export Audited Expected Loss & Risk Pricing Report
df.to_csv("expected_loss_report.csv")
print("\n[SUCCESS] Audited report exported to expected_loss_report.csv")

#Executive Portfolio Provisioning Metric
is_approved = df["Decision"].str.contains("APPROVED")
approved_exposure = df.loc[is_approved, "EAD"].sum()
approved_el = df.loc[is_approved, "Expected_Loss"].sum()

print("\n=== EXECUTIVE BASEL II PROVISIONING SUMMARY ===")
print(f"Total Approved Capital Exposure : INR {approved_exposure:,.2f}")
print(f"Mandatory Basel Loss Provision:   INR {approved_el:,.2f}")
print(f"Portfolio Expected Loss Rate:     {(approved_el / approved_exposure) * 100:,.2f}%")
