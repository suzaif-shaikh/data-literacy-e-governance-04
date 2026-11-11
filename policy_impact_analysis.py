"""
Policy Impact Analysis - Digital Public Service Expansion
Run:
    pip install pandas numpy matplotlib openpyxl
    python policy_impact_analysis.py

The workbook dataset is synthetic/hypothetical for learning; it is not official data.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "Policy_Impact_Analysis.xlsx"
OUTPUT_DIR = Path("python_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_excel(INPUT_FILE, sheet_name="Cleaned_Data")
print("Rows:", len(df))
print("Missing values by column:\n", df.isna().sum())

yearly = df.groupby("Year").agg(
    Total_Transactions=("Service_Transactions", "sum"),
    Avg_Online_Share=("Online_Service_Share_Pct", "mean"),
    Avg_Processing_Days=("Average_Processing_Days", "mean"),
    Avg_Satisfaction=("Citizen_Satisfaction_Pct", "mean"),
    Avg_Complaints_Resolved=("Complaints_Resolved_Pct", "mean")
).reset_index()

yearly["YoY_Transaction_Growth_Pct"] = (
    yearly["Total_Transactions"].pct_change() * 100
).round(2)

state = df.groupby("State").agg(
    Total_Transactions=("Service_Transactions", "sum"),
    Avg_Online_Share=("Online_Service_Share_Pct", "mean"),
    Avg_Processing_Days=("Average_Processing_Days", "mean"),
    Avg_Satisfaction=("Citizen_Satisfaction_Pct", "mean")
).reset_index().sort_values("Total_Transactions", ascending=False)

print("\nYEARLY KPI SUMMARY\n", yearly.to_string(index=False))
print("\nSTATE SUMMARY\n", state.to_string(index=False))

yearly.to_csv(OUTPUT_DIR / "yearly_kpi_summary.csv", index=False)
state.to_csv(OUTPUT_DIR / "state_analysis.csv", index=False)

plt.figure(figsize=(8, 5))
plt.plot(yearly["Year"], yearly["Total_Transactions"], marker="o")
plt.title("Total Digital Public Service Transactions by Year")
plt.xlabel("Year")
plt.ylabel("Transactions")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "transactions_trend.png", dpi=150)
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(state["State"], state["Total_Transactions"])
plt.title("Cumulative Transactions by State")
plt.xlabel("State")
plt.ylabel("Transactions")
plt.xticks(rotation=40, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "state_comparison.png", dpi=150)
plt.show()
