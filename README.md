# JFA-Regulatory: Prudential Credit Risk & Basel II Capital Adequacy Engine

A self-directed learning project modelling Basel II regulatory capital calculations, RBNZ-aligned stress testing, and interactive credit risk dashboarding on a synthetic retail lending portfolio. Built end to end in Python with SQLite persistence and Streamlit visualisation.

---

## Key Results

| Metric | Value |
|:---|:---|
| Portfolio Size | 20 retail borrowers (synthetic) |
| Regulatory Framework | Basel II Capital Adequacy Ratio (CAR) |
| Stress Test Range | +300 to +500 bps interest rate shock |
| NZ Benchmarks Used | ANZ 12.5%, ASB 12.0%, BNZ 11.5%, RBNZ minimum 8.0% |
| Dashboard | Interactive Streamlit with live heatmaps & underwriting intake |

## What This Project Covers

1. **Loan Origination Engine** — Multi-factor CIBIL score and FOIR (Fixed Obligation to Income Ratio) underwriting rules for automated approve/reject decisioning.
2. **Vectorised Portfolio Processing** — Batch underwriting across the full portfolio using Pandas vectorisation (no row-by-row loops).
3. **Credit Risk Tier Segmentation** — Prime / Near-Prime / Sub-Prime stratification with named `.groupby()` aggregation and capital concentration metrics.
4. **Macroeconomic Stress Testing** — +300 bps rate shock simulation calculating stressed EMI, stressed FOIR, and resilience classification (Resilient / Vulnerable / Baseline Rejection).
5. **Basel II Expected Loss Engine** — EL = PD × LGD × EAD with dynamic risk-adjusted pricing and capital provisioning.
6. **Master Risk Ledger & Heatmap** — Consolidated 20-column risk ledger with Seaborn Expected Loss heatmap.
7. **CLI Audit Pipeline** — `python jfa_cli.py audit` for automated end-to-end portfolio processing.
8. **SQLite Database Integration** — Persistent storage via `jfa_risk.db` with decoupled ETL (`init_db`) and query gateway (`load_portfolio`).
9. **Interactive Underwriting Intake** — Real-time applicant submission form with instant risk scoring and reactive dashboard recalculation.
10. **Capital Adequacy Ratio (CAR)** — Dynamic RWA mapping (0.50 / 1.00 / 1.50 risk weights) with Tier-1 capital slider benchmarked against NZ Big 4 banks.

## Project Structure

```
├── #Jadhav Financial lab Day-1.py   # Day 1: Initial loan engine
├── JFA.py                           # Day 2: CIBIL & FOIR underwriting
├── JFA_portfolio.py                 # Day 3: Vectorised batch processing
├── JFA_charts.py                    # Day 4: Capital exposure & risk scatter
├── JFA_segmentation.py              # Day 5: Risk tier stratification
├── JFA_stress_test.py               # Day 6: Macroeconomic shock simulation
├── JFA_Expected_loss.py             # Day 7: Basel II EL engine
├── JFA_masterDashboard.py           # Day 8: Master risk ledger
├── jfa_cli.py                       # Day 9: CLI audit pipeline
├── JFA_narrative.py                 # Day 9: Credit committee narrative
├── JFA_database.py                  # Day 13-16: SQLite gateway & CAR
├── app.py                           # Day 10-16: Streamlit dashboard
├── jfa_risk.db                      # Persistent SQLite database
├── portfolio.csv                    # Source portfolio data
├── master_risk_ledger.csv           # Consolidated risk output
├── master_risk_heatmap.png          # Basel EL heatmap
└── DAY-*-FINAL-LOCK.md              # Daily build logs with verified metrics
```

## How to Run

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn streamlit

# Launch the interactive credit risk dashboard
streamlit run app.py

# Or run the CLI audit pipeline
python jfa_cli.py audit
```

## Tech Stack

Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit · SQLite · Basel II Framework

## Author

**Raj Dwarkanath Jadhav** — [GitHub](https://github.com/Rajjadhav555) · [LinkedIn](https://linkedin.com/in/raaj-jadhav)
