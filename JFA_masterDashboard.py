import pandas as pd

df_stress = pd.read_csv("stressed_portfolio_report.csv")
df_el = pd.read_csv("expected_loss_report.csv")

el_cols = ["Applicant_ID", "PD", "LGD", "Expected_Loss", "fair_risk_rate", "Pricing_Delta"]
df_master = pd.merge(df_stress, df_el[el_cols], on="Applicant_ID")
print(df_master.info())
df_master.to_csv("master_risk_ledger.csv", index=False)
print("\n[SUCCESS] Master Risk Ledger exported to master_risk_ledger.csv")

import matplotlib.pyplot as plt
import seaborn as sns

risk_matrix = df_master.pivot_table(index="Decision", columns="PD", values="Expected_Loss", aggfunc="sum", fill_value=0)
print("\n===     EXECUTIVE RISK MATRIX (EXPECTED LOSS)      ===")
print(risk_matrix)
plt.figure(figsize=(8,4))
sns.heatmap(risk_matrix, annot=True, fmt=",.0f", cmap="YlOrRd")
plt.title("Executuive Credit Risk Matrix: Decision vs Default Probablity")
plt.tight_layout()
plt.savefig("master_risk_heatmap.png")