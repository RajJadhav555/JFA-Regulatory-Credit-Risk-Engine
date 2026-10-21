import pandas as pd

df = pd.read_csv("master_risk_ledger.csv")
approved = df[df["Decision"].str.contains("APPROVED")]
rejected = df[~df["Decision"].str.contains("APPROVED")]

approved_capital = approved["Principal"].sum()
rejected_capital = rejected["Principal"].sum()

approved_el = approved["Expected_Loss"].sum()
resilient_count = (approved["Stressed_Status"] == "RESILIENT: Absorbed shock").sum()
total_approved = len(approved)
approval_rate = round((total_approved) / len(df) * 100, 1)

memo = (
        f"\n======================================================\n"
        f"     EXECUTIVE CREDIT RISK MEMORANDUM (CREDIT COMMITTEE)\n"
        f"======================================================\n"
        f"1. CAPITAL EXPOSURE & APPROVAL:\n"
        f"   - Total Approved: INR {approved_capital:,.2f} ({approval_rate}% approval rate across {len(df)} applicants).\n"
         f"   - Capital Intercepted: INR {rejected_capital:,.2f} of high-risk applications rejected.\n"
        f"2. BASEL II PROVISIONING & REGULATORY RESERVES:\n"
        f"   - Mandatory Provisioning: INR {approved_el:,.2f} set aside for baseline expected loss.\n"
        f"3. MACROECONOMIC STRESS RESILIENCE (+300 BPS):\n"
        f"   - Resilience Rate: {resilient_count}/{total_approved} approved loans fully absorbed shock.\n"
)
print(memo)

with open("credit_committee_memo.txt", "w") as f:
    f.write(memo)
print("[SUCCESS] Credit Committee Memorandum exported to credit_committee_memo.txt")