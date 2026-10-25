import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jadhav Financial Analytics", layout="wide")
st.title("Jadhav Financial Analytics: Credit Risk Dashboard")

from JFA_database import load_portfolio
df = load_portfolio()
status_filter = st.sidebar.radio("Filter by Decision", ["ALL", "APPROVED", "REJECTED"])

if status_filter != "ALL":
    filtered_df = df[df["Decision"].str.contains(status_filter)]
else: 
    filtered_df = df

approved_cap = df[df["Decision"].str.contains("APPROVED")]["Principal"].sum()
rejected_cap = df[df["Decision"].str.contains("REJECTED")]["Principal"].sum()
loss_reserved = df[df["Decision"].str.contains("APPROVED")]["Expected_Loss"].sum()
approval_rate = (len(df[df["Decision"].str.contains("APPROVED")]) / len(df)) * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Approved Capital", f"INR {approved_cap:,.0f}")
k2.metric("Intercepted Risk", f"INR {rejected_cap:,.0f}")
k3.metric("Mandatory Basel Provision", f"INR {loss_reserved:,.0f}")
k4.metric("Approval Rate", f"{approval_rate:.1f}%")

st.sidebar.header("Macro Risk Simulation")
shock_bps = st.sidebar.slider("Rate Shock (Basis Points)", 0, 500, 300, 50)
st.sidebar.info(f"simulating **+{shock_bps} bps** RBNZ Macro Stress Scenario")

shock_pct = shock_bps / 100.0
r = (df["Rate"] + shock_pct) / (12 * 100)
n = df["Tenure_Years"] * 12
df["Simulated_EMI"] = round(df["Principal"] * r * ((1 + r)**n) / (((1 + r)**n) - 1), 2)
df["Simulated_FOIR_%"] = round((df["Simulated_EMI"] / df["Monthly_Income"]) * 100, 2)

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.subheader("Executive Risk Heatmap Matrix")
    st.image("master_risk_heatmap.png", use_container_width=True)

with col_right:
    st.subheader("Individual Applicant Drill-Down")
    selected_applicant = st.selectbox("Select Borrower for Audit", df["Name"].unique())
    borrower = df[df["Name"] == selected_applicant].iloc[0]

    b_col1, b_col2, b_col3 = st.columns(3)
    b_col1.metric("Monthly Income", f"INR  {borrower['Monthly_Income']:,.0f}")
    b_col2.metric("CIBIL Score", f"{int(borrower['CIBIL'])}")
    b_col3.metric("Debt Ratio (FOIR)", f"{borrower['FOIR_%']:.1f}%")

    if "APPROVED" in borrower["Decision"]:
        st.success(f"Underwriting Decision: {borrower['Decision']}")
    else:
        st.error(f"Underwriting Decision: {borrower['Decision']}")

    s_col1, s_col2, s_col3 = st.columns(3)
    s_col1.metric("Baseline Monthly EMI", f"INR {borrower['Monthly_EMI']:,.2f}")
    s_col2.metric(f"Stressed EMI(+{shock_bps} bps)", f"INR {borrower['Simulated_EMI']:,.2f}")
    s_col3.metric("Basel Expected Loss", f"INR {borrower['Expected_Loss']:,.0f}")


    with st.expander("📄 View Credit Committee Audit Memo"):
        with open("credit_committee_memo.txt") as f:
            st.text(f.read()) 

with st.expander("📋 View Complete Master Risk Ledger & Stress Scenarios"):
        st.subheader("Master Risk Ledger")
        st.dataframe(filtered_df)
        st.subheader(f"Live Macro Shock Impact (+{shock_bps} bps)")
        sim_view = ["Name", "Decision", "Monthly_EMI", "Simulated_EMI", "FOIR_%", "Simulated_FOIR_%"]
        sim_filtered = df[df["Decision"].str.contains(status_filter)] if status_filter != "ALL" else df
        st.dataframe(sim_filtered[sim_view])