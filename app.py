import streamlit as st
import pandas as pd

st.title("Jadhav Financial Analytics: Credit Risk Dashboard")

df = pd.read_csv("master_risk_ledger.csv")
status_filter = st.sidebar.radio("Filter by Decision", ["ALL", "APPROVED", "REJECTED"])

if status_filter != "ALL":
    filtered_df = df[df["Decision"].str.contains(status_filter)]
else: 
    filtered_df = df

st.subheader("Master Risk Ledger")
st.dataframe(filtered_df)

approved_cap = df[df["Decision"].str.contains("APPROVED")]["Principal"].sum()
loss_reserved = df[df["Decision"].str.contains("APPROVED")]["Expected_Loss"].sum()

col1,col2 = st.columns(2)
col1.metric("Approved Capital Exposure", f"INR {approved_cap:,.0f}")
col2.metric("Mandatory Basel Provision", f"INR {loss_reserved:,.0f}")

st.subheader("Executive Risk Heatmap Matrix")
st.image("master_risk_heatmap.png", caption="Portfolio Expected Loss Matrix by Decision & Basel PD")

st.sidebar.header("Macro Risk Simulation")
shock_bps = st.sidebar.slider("Rate Shock (Basis Points)", 0, 500, 300, 50)
st.sidebar.info(f"simulating **+{shock_bps} bps** RBNZ Macro Stress Scenario")

shock_pct = shock_bps / 100.0
r = (df["Rate"] +  shock_pct) / (12 * 100)
n = df["Tenure_Years"] *12
df["Simulated_EMI"] = round(df["Principal"] * r * ((1 + r)**n) / (((1 + r)**n) -1), 2)
df["Simulated_FOIR_%"] = round((df["Simulated_EMI"] / df["Monthly_Income"]) * 100, 2)

st.subheader(f"Live Macro Shock Impact(+{shock_bps} bps)")
sim_view = ["Name", "Decision", "Monthly_EMI", "Simulated_EMI", "FOIR_%", "Simulated_FOIR_%"]
sim_filtered = df[df["Decision"].str.contains(status_filter)] if status_filter != "ALL" else df
st.dataframe(sim_filtered[sim_view])

with st.expander("📄 View Credit Committee Audit Memo"):
    with open("credit_committee_memo.txt") as f:
        st.text(f.read()) 