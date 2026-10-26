import sqlite3
import pandas as pd

DB_NAME = "jfa_risk.db"

def init_db():
    df = pd.read_csv("master_risk_ledger.csv")
    with sqlite3.connect(DB_NAME) as conn:
        df.to_sql("portfolio_ledger", conn, if_exists="replace", index=False)
    print("Database Initialized portfolio_ledger table created successfully.")

def load_portfolio():
    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql("SELECT * FROM portfolio_ledger", conn)

def underwrite_applicant(name, principal, rate, tenure_years, monthly_income, cibil):
    r = rate / (12 * 100)
    n = tenure_years * 12
    emi = round(principal * r * ((1 + r)**n) / (((1 + r)**n) -1), 2)
    foir = round((emi / monthly_income) * 100, 2)

    if cibil < 650:
        decision = "REJECTED: Low CIBIL (<650)"
    elif foir > 50.0:
        decision = "REJECTED: High FOIR (>50.0)"
    elif cibil >= 750:
        decision = "APPROVED: Prime Borrower"
    else: 
        decision = "CONDITIONAL: Need Guarantor"

    pd_val = 0.02 if cibil >= 750 else (0.05 if cibil >= 700 else (0.12 if cibil >= 650 else 0.25))
    lgd = 0.45
    expected_loss = round(pd_val * lgd * principal, 2)
    s_r = (rate + 3.0) / (12 * 100)
    s_emi = round(principal * s_r * ((1 + s_r)**n) / (((1 + s_r)**n) - 1),2)
    s_foir = round((s_emi / monthly_income) * 100, 2)
    s_status = "UNAFFECTED: Baseline Rejection" if "REJECTED" in decision else ("RESILIENT: Absorbed shock" if s_foir <= 50.0 else "VULNERABLE: Breached 50%")
    fair_risk_rate = round(7.0 + 2.0 + (expected_loss / principal * 100), 2)
    pricing_delta = round(rate - fair_risk_rate, 2)
    emi_shock_delta = round(s_emi - emi, 2)
    foir_shock_delta = round(s_foir - foir, 2)
    portfolio = load_portfolio()
    new_id = int(portfolio["Applicant_ID"].max() + 1 ) if not portfolio.empty else 101

    new_data = {
        "Applicant_ID":new_id, "Name": name, "Principal": principal, "Rate": rate,
        "Tenure_Years": tenure_years, "Monthly_Income": monthly_income, "CIBIL": cibil,
        "Monthly_EMI": emi, "FOIR_%": foir, "Decision": decision,
        "Stressed_EMI": s_emi, "Stressed_FOIR_%": s_foir, "Stressed_Status": s_status,
        "EMI_Shock_Delta": emi_shock_delta, "FOIR_Shock_Delta": foir_shock_delta,
        "PD": pd_val, "LGD": lgd, "Expected_Loss": expected_loss,
        "fair_risk_rate": fair_risk_rate, "Pricing_Delta": pricing_delta
    }

    with sqlite3.connect(DB_NAME) as conn:
        pd.DataFrame([new_data]).to_sql("portfolio_ledger", conn, if_exists="append", index=False)

    return decision
if __name__ == "__main__":
    init_db()
    test_df = load_portfolio()
    print(f"Verified: Successfully loaded {len(test_df)} rows from SQLite.")