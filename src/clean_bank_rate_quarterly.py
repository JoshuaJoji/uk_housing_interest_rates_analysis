import os
import pandas as pd

os.makedirs("data/clean", exist_ok=True)

df = pd.read_csv("data/raw/bank_rate.csv")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Bank Rate"] = pd.to_numeric(df["Bank Rate"], errors="coerce")

df = df.dropna(subset=["Date", "Bank Rate"]).sort_values("Date")

df = df[df["Date"].dt.year >= 2011]

df["Year"] = df["Date"].dt.year
df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)

quarterly = (
    df.groupby(["Year", "Quarter"], as_index=False)["Bank Rate"]
      .mean()
      .round(4)
      .rename(columns={"Bank Rate": "Bank_Rate_Quarterly_Avg"})
      .sort_values(["Year", "Quarter"])
)
output_path = "data/clean/bank_rate_quarterly.csv"
quarterly.to_csv(output_path, index=False)

print(quarterly.head(8))
print(f"Rows saved: {len(quarterly)}")
print(f"Saved: {output_path}")