import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("underwritten_portfolio.csv")

approved = df[df["Decision"].str.contains("APPROVED")]["Principal"].sum()
rejected = df[df["Decision"].str.contains("REJECTED")]["Principal"].sum()

print(f"Sanctioned Capital: ₹ {approved:,.2f}")
print(f"Rejected Capital: ₹ {rejected:,.2f}")

categories = ["Sanctioned", "Rejected"]
amounts = [approved, rejected]

plt.bar(categories,amounts, color=["green", "crimson"])

plt.title("Jadhav Financial Labs: Capital Exposure")
plt.ylabel("Capital Amount in INR(₹)")
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.savefig("capital_exposure.png")

plt.figure(figsize=(8,5))
plt.scatter(df[df["Decision"].str.contains("APPROVED")]["CIBIL"], df[df["Decision"].str.contains("APPROVED")]["FOIR_%"], color="green", s=120)
plt.scatter(df[df["Decision"].str.contains("REJECTED")]["CIBIL"], df[df["Decision"].str.contains("REJECTED")]["FOIR_%"], color="crimson", s=120)
plt.axhline(y=50, color="darkorange", linestyle="--")
plt.axvline(x=650, color="red", linestyle="--")
plt.title("Portfolio Risk Distribution: CIBIL vs FOIR")
plt.xlabel("CIBIL score")
plt.ylabel("FOIR %")
plt.savefig("risk_scatter.png")

  