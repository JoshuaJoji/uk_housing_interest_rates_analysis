import pandas as pd
import os


def aggregate_bank_rate_yearly(
    input_path="data/clean/bank_rate_quarterly.csv",
    output_path="data/processed/bank_rate_yearly_avg.csv",
):
    df = pd.read_csv(input_path)

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Bank_Rate_Quarterly_Avg"] = pd.to_numeric(
        df["Bank_Rate_Quarterly_Avg"], errors="coerce"
    )

    df = df.dropna(subset=["Year", "Bank_Rate_Quarterly_Avg"])

    yearly = (
        df.groupby("Year")["Bank_Rate_Quarterly_Avg"]
        .mean()
        .reset_index()
        .rename(columns={"Bank_Rate_Quarterly_Avg": "Bank_Rate_Yearly_Avg"})
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    yearly.to_csv(output_path, index=False)

    print("Saved:", output_path)
    print(yearly.head())


if __name__ == "__main__":
    aggregate_bank_rate_yearly()
