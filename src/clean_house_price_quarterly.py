import os
import pandas as pd

os.makedirs("data/clean", exist_ok=True)

df = pd.read_csv(
    "data/raw/uk_house_price_annual_average_price.csv",
    skiprows=1,
    header=None
)
df = df.iloc[:, :2]
df.columns = ["Month", "UK_Average_House_Price"]

df["Date"] = pd.to_datetime(df["Month"], format="%b %Y", errors="coerce")

df["UK_Average_House_Price"] = (
    df["UK_Average_House_Price"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["UK_Average_House_Price"] = pd.to_numeric(
    df["UK_Average_House_Price"], errors="coerce"
)

df = df.dropna(subset=["Date", "UK_Average_House_Price"])

df = df[df["Date"].dt.year >= 2011]

df["Year"] = df["Date"].dt.year
df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)

clean_df = (
    df.groupby(["Year", "Quarter"], as_index=False)["UK_Average_House_Price"]
      .mean()
      .round(0)
      .sort_values(["Year", "Quarter"])
      .reset_index(drop=True)
)

clean_df["UK_Average_House_Price"] = clean_df["UK_Average_House_Price"].astype(int)

output_path = "data/clean/uk_house_price_quarterly.csv"
clean_df.to_csv(output_path, index=False)

print(clean_df.head(8))
print(f"Rows saved: {len(clean_df)}")
print(f"Saved: {output_path}")