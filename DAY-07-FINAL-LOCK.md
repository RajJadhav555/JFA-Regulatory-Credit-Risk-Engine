# 🏛️ MASTER PROGRESS LEDGER: DAY 7 COMPLETE
**Date:** October 19, 2026  
**Operator:** Raj Dwarkanath Jadhav  
**Mission:** Operation Auckland (120-Day Protocol) — Day 7 Locked  
**File Created:** [`JFA_Expected_loss.py`](file:///media/raaj-jadhav/HDD/files/Jadhav/JFA_Expected_loss.py)  
**Report Exported:** [`expected_loss_report.csv`](file:///media/raaj-jadhav/HDD/files/Jadhav/expected_loss_report.csv)  

---

## 🏆 Day 7 Accomplishments (Hand-Crafted & Manually Executed)

1. **Independent Real-Time Debugging**:
   - Diagnosed and resolved `KeyError` on column names and `AttributeError` (`containes` ➔ `contains`) with zero hesitation.
   - 100% manual code entry with complete line-by-line ownership.

2. **Basel II / III Expected Loss Framework Implementation**:
   - Built the institutional mathematical engine:
     $$\text{Expected Loss (EL)} = \text{PD} \times \text{EAD} \times \text{LGD}$$
   - **PD (Probability of Default) Calibration:** Vectorized CIBIL scoring tiers via `np.select`:
     * Prime ($\ge 750$): $2.0\%$ default probability
     * Near-Prime ($700 - 749$): $5.0\%$ default probability
     * Subprime ($650 - 699$): $12.0\%$ default probability
     * High Risk ($< 650$): $25.0\%$ default probability
   - **EAD (Exposure at Default):** Linked to sanctioned facility balances.
   - **LGD (Loss Given Default):** Calibrated to international unsecured retail benchmark ($45.0\%$).

3. **Risk-Adjusted Dynamic Pricing Engine**:
   - Integrated Cost of Funds ($7.0\%$) and Target Profit Margin ($2.0\%$) with dynamically calculated Credit Risk Premiums (`EL_Rate_%`).
   - Quantified Pricing Deltas:
     * **Aarav Sharma:** Fair risk rate $9.90\%$ vs actual $10.50\%$ (+$0.60\%$ profitable bank spread).
     * **Priya Patil:** Fair risk rate $20.25\%$ vs requested $9.00\%$ ($-11.25\%$ toxic underpricing—confirming Day 3 rejection).
     * **Ananya Joshi:** Fair risk rate $20.25\%$ vs requested $10.00\%$ ($-10.25\%$ toxic underpricing).

4. **Executive Basel II Capital Provisioning**:
   - **Total Approved Capital Exposure:** INR 3,000,000.00
   - **Mandatory Day 1 Basel Loss Provision:** INR 27,000.00
   - **Portfolio Expected Loss Rate:** $0.90\%$
   - Exported audited ledger to [`expected_loss_report.csv`](file:///media/raaj-jadhav/HDD/files/Jadhav/expected_loss_report.csv).

---

## 🎙️ The 3-Sentence Auckland Interview Story (Day 7)

1. *"While baseline underwriting gates approvals, global banking standards under Basel II / III require institutional lenders to provision capital against statistical default on Day 1."*
2. *"I built an institutional Expected Loss engine ($EL = PD \times EAD \times LGD$) calibrating default probabilities from credit scores and standardizing loss-given-default at 45% for unsecured facilities."*
3. *"This quantified a mandatory ₹27,000 loss reserve across our ₹3,000,000 approved book and powered a risk-adjusted pricing engine that exposed severe underpricing (-11.25%) on rejected high-risk applicants."*

---

## 🚀 Day 8 Agenda: Comprehensive Risk Analytics Dashboard & Heatmaps
1. Consolidating baseline underwriting, macroeconomic stress delta, and Basel Expected Loss into an end-to-end Master Executive Risk Ledger.
2. Building an automated visual risk heatmap (PD vs. LGD vs. Capital Exposure) for credit committees and RBNZ regulatory audits.
