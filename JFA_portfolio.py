#Jadhav Financial Group - Portfolio Credit Underwriting Engine
#Author : Raj Jadhav
#Mission: Operation Auckland Day 3

import pandas as pd
import numpy as np

#Ingest Loan Portfolio

df = pd.read_csv("portfolio.csv")

print("==================================================================")
print("             JADHAV FINANCIAL LAB - INGESTED PORTFOLIO            ")
print("==================================================================")
print(df)

#Vectorized Monthly Rate (r) and  Total months (n)

monthly_rate = df["Rate"] / (12 *100)
total_months = df["Tenure_Years"] * 12

#Vecotized EMI formula across all the applicants simulteneously

df["Monthly_EMI"] = round(
    df["Principal"] * monthly_rate * ((1 + monthly_rate) ** total_months) / 
    (((1 + monthly_rate) ** total_months) - 1),
    2

)

#Vetorized FOIR (Debt Burden Ratio)
df["FOIR_%"] = round((df["Monthly_EMI"] / df["Monthly_Income"]) * 100, 2)

print("\n==================================================================")
print("             PORTFOLIO WITH COMPUTED EMI & FOIR BURDEN            ")
print("==================================================================")
print(df[["Applicant_ID", "Name", "Principal", "Monthly_EMI", "FOIR_%", "CIBIL"]])

#Define the underwriting condition

conditions = [
    df["CIBIL"] < 650,                                                  #Gate 1: Hard CIBIL cut-off
    df["FOIR_%"] > 50.0,                                                #Gate 2: High Debt Burden
    (df["CIBIL"] >= 750) & (df["FOIR_%"] <= 50.0),                      #Gate 3: Prime Borrower
    (df["CIBIL"] >= 650) & (df["CIBIL"] < 750) & (df["FOIR_%"] <= 50.0) #Gate 4: Moderate Risk
]

#Defime the corresponding bank decisions
decisions = [
    "REJECTED: Low CIBIL(<650)",
    "REJECTED: High FOIR (>50.0)",
    "APPROVED: Prime Borrower",
    "CONDITIONAL: Needs Guarantor"
]


#Apply decisions across the entire potfolio in one shot

df["Decision"] = np.select(conditions, decisions, default="UNDER_REVIEW")

#Display Final Underwriting Result

print("\n==================================================================")
print("             JADHAV FINANCIAL LAB - UNDERWRITING DECISIONS        ")
print("==================================================================")
cols_to_show = ["Applicant_ID", "Name", "Monthly_Income", "Monthly_EMI", "FOIR_%", "CIBIL", "Decision"]
print(df[cols_to_show].to_string(index = False))

#Capital Exposure Metrics
total_requested = df["Principal"].sum()
approved_mask = df["Decision"].str.startswith("APPROVED")
conditional_mask = df["Decision"].str.startswith("CONDITIONAL")
sanctioned_mask = approved_mask | conditional_mask

total_sanctioned = df.loc[sanctioned_mask, "Principal"].sum()
total_rejected = df.loc[~sanctioned_mask, "Principal"].sum()

#Portfolio Risk Ratio
approval_rate = round(sanctioned_mask.sum() / len(df) * 100, 2)
rejection_rate = round((100 - approval_rate), 2)
avg_portfolio_foir = round(df["FOIR_%"].mean(), 2)

print("\n" + "=" * 66)
print("             EXECUTIVE RISK & EXPOSURE SUMMARY")
print("==================================================================")
print(f"Total Applications Processed: {len(df)}")
print(f"Total Capital Requested: ₹ {total_requested:,.2f}")
print(f"Total Capital Sanctioned: ₹ {total_sanctioned:,.2f}")
print(f"Total Capital Rejected: ₹ {total_rejected:,.2f}")
print(f"Portfolio Approval Rate: {approval_rate} %")
print(f"Portfolio Rejection Rate: {rejection_rate} %")
print(f"Average Borrower FOIR: {avg_portfolio_foir} %")

#Export Final Audited Portfolio to CSV
df.to_csv("underwritten_portfolio.csv", index=False)
print("\n Audited Underwrited Ledger Exported to 'underwritten_portfolio.csv'\n")
