import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Jadhav Financial Analytics", layout="wide")
st.title("Jadhav Financial Analytics: Credit Risk Dashboard")
filter_options = ["🌐 ALL PORTFOLIO", "✅ APPROVED BOOK", "❌ REJECTED COHORT"]
selected_scope = st.radio("Portfolio Scope Lens", filter_options, horizontal=True)
status_filter = "APPROVED" if "APPROVED" in selected_scope else ("REJECTED" if "REJECTED" in selected_scope else "ALL")


from JFA_database import load_portfolio, underwrite_applicant, calculate_car
df = load_portfolio()



approved_cap = df[df["Decision"].str.contains("APPROVED")]["Principal"].sum()
rejected_cap = df[df["Decision"].str.contains("REJECTED")]["Principal"].sum()
loss_reserved = df[df["Decision"].str.contains("APPROVED")]["Expected_Loss"].sum()
approval_rate = (len(df[df["Decision"].str.contains("APPROVED")]) / len(df)) * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Approved Capital", f"${approved_cap:,.0f}")
k2.metric("Intercepted Risk", f"${rejected_cap:,.0f}")
k3.metric("Mandatory Basel Provision", f"${loss_reserved:,.0f}")
k4.metric("Approval Rate", f"{approval_rate:.1f}%")

st.sidebar.header("🏦Capital Adequacy Test")
sim_tier1 = st.sidebar.slider("Tier-1 Bank Capital (NZD $)", 50000, 10000000, 5000000, 50000)
bank_targets = {
        "🏛️ RBNZ Statutory (8.0%)": 8.0,
        "🔵 ANZ New Zealand (12.5%)": 12.5,
        "🟡 ASB Bank (12.0%)": 12.0,
        "🔴 BNZ Bank (11.5%)": 11.5,
        "🔴 Westpac NZ (12.0%)": 12.0
    }
selected_bank = st.sidebar.selectbox("Bank Capital Target Lens", list(bank_targets.keys()))
target_floor = bank_targets[selected_bank]

car_data = calculate_car(tier1_capital=sim_tier1)
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏦 Tier-1 Capital", f"${car_data['tier1']:,.0f}")
c2.metric("⚖️ Risk-Weighted Assets", f"${car_data['total_rwa']:,.0f}")
c3.metric("📈 CAR %", f"{car_data['car_pct']:.1f}%")
if car_data["car_pct"] < target_floor:
    shortfall = round(sim_tier1 - ((target_floor / 100.0) * car_data["total_rwa"]), 2)
    c4.metric(f"🚨 {selected_bank.split()[1]} SHORTFALL", f"${shortfall:,.0f}", delta=f"{car_data['car_pct'] - target_floor:.1f}% Below Target", delta_color="inverse")
elif car_data["car_pct"] < target_floor + 2.0:
    c4.metric("⚠️ Buffer Warning", f"${car_data['headroom']:,.0f}", delta="Close to Target", delta_color="off")
else:
    c4.metric(f"💚 {selected_bank.split()[1]} Compliant", f"${car_data['headroom']:,.0f}", delta=f"+{car_data['car_pct'] - target_floor:.1f}% Headroom")

st.sidebar.header("Macro Risk Simulation")
shock_bps = st.sidebar.slider("Rate Shock (Basis Points)", 0, 500, 300, 50)
st.sidebar.info(f"simulating **+{shock_bps} bps** RBNZ Macro Stress Scenario")

st.sidebar.header("📝 New Loan Application Intake")
with st.sidebar.form("intake_form"):
    new_name = st.text_input("Applicant Name", "Raj Jadhav")
    new_principal = st.number_input("Loan Amount", min_value=10000, max_value=10000000, value=500000, step=50000)
    new_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=30.0, value=10.5, step=0.25)
    new_tenure = st.number_input("Tenure (Years)", min_value=1, max_value=30, value=3, step=1)
    new_income = st.number_input("Monthly Income", min_value=5000, max_value=5000000, value=75000, step=5000)
    new_cibil = st.number_input("CIBIL Score", min_value=300, max_value=900, value=780, step=10)
    submit_btn = st.form_submit_button("⚡ Underwrite & Commit to SQL")

if submit_btn:
    decision_result = underwrite_applicant(new_name, new_principal, new_rate, new_tenure, new_income, new_cibil)
    st.sidebar.success(f"Underwritten: {decision_result}")
    st.rerun()


shock_pct = shock_bps / 100.0
r = (df["Rate"] + shock_pct) / (12 * 100)
n = df["Tenure_Years"] * 12
df["Simulated_EMI"] = round(df["Principal"] * r * ((1 + r)**n) / (((1 + r)**n) - 1), 2)
df["Simulated_FOIR_%"] = round((df["Simulated_EMI"] / df["Monthly_Income"]) * 100, 2)
filtered_df = df[df["Decision"].str.contains(status_filter)] if status_filter != "ALL" else df
col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.subheader("Executive Risk Heatmap Matrix")
    fig, ax = plt.subplots(figsize =(6, 4))
    matrix = filtered_df.pivot_table(index="Decision", columns="PD", values="Expected_Loss", aggfunc="sum", fill_value=0)
    sns.heatmap(matrix, annot=True, fmt=",.0f", cmap="YlOrRd", ax=ax, cbar=False)
    plt.tight_layout()
    st.pyplot(fig)

with col_right:
    st.subheader("Individual Applicant Drill-Down")
    selected_applicant = st.selectbox("Select Borrower for Audit", filtered_df["Name"].unique())
    borrower = filtered_df[filtered_df["Name"] == selected_applicant].iloc[0]

    b_col1, b_col2, b_col3 = st.columns(3)
    b_col1.metric("Monthly Income", f"${borrower['Monthly_Income']:,.0f}")
    b_col2.metric("Credit Score", f"{int(borrower['CIBIL'])}")
    b_col3.metric("Debt Ratio (FOIR)", f"{borrower['FOIR_%']:.1f}%")

    if "APPROVED" in borrower["Decision"]:
        st.success(f"Underwriting Decision: {borrower['Decision']}")
    else:
        st.error(f"Underwriting Decision: {borrower['Decision']}")

    s_col1, s_col2, s_col3 = st.columns(3)
    s_col1.metric("Baseline Monthly EMI", f"${borrower['Monthly_EMI']:,.2f}")
    s_col2.metric(f"Stressed EMI(+{shock_bps} bps)", f"${borrower['Simulated_EMI']:,.2f}")
    s_col3.metric("Basel Expected Loss", f"${borrower['Expected_Loss']:,.0f}")


    with st.expander("📄 View Credit Committee Audit Memo"):
            with open(BASE_DIR / "credit_committee_memo.txt") as f:
                st.text(f.read()) 

with st.expander("📋 View Complete Master Risk Ledger & Stress Scenarios"):
        st.subheader("Master Risk Ledger")
        st.dataframe(filtered_df)
        st.subheader(f"Live Macro Shock Impact (+{shock_bps} bps)")
        sim_view = ["Name", "Decision", "Monthly_EMI", "Simulated_EMI", "FOIR_%", "Simulated_FOIR_%"]
        sim_filtered = df[df["Decision"].str.contains(status_filter)] if status_filter != "ALL" else df
        st.dataframe(sim_filtered[sim_view])