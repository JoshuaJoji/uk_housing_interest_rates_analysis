import pandas as pd
import os


def clean_and_average_cpi(
    input_path="data/raw/CPI_quarterly.csv",
    output_path="data/clean/cpi_quarterly_avg.csv",
):
    df = pd.read_csv(input_path)
    df = df.iloc[455:].reset_index(drop=True)

    df.columns = [c.strip() for c in df.columns]

    date_col = df.columns[0]
    value_col = df.columns[1]

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    df["Year"] = df[date_col].dt.year
    df["Quarter"] = df[date_col].dt.quarter

    df = df.rename(columns={value_col: "CPI_Index"})


    df = df[["Year", "Quarter", "CPI_Index"]]

    df["Year"] = df["Year"].astype(int)
    df["Quarter"] = df["Quarter"].astype(int)
    df["CPI_Index"] = pd.to_numeric(df["CPI_Index"], errors="coerce")

    df = df.dropna().reset_index(drop=True)

    quarterly_avg = (
        df.groupby(["Year", "Quarter"])["CPI_Index"]
        .mean()
        .reset_index()
        .rename(columns={"CPI_Index": "CPI_Quarterly_Avg"})
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    quarterly_avg.to_csv(output_path, index=False)

    print(quarterly_avg.head())
    print(f"Rows: {len(quarterly_avg)}")


if __name__ == "__main__":
    clean_and_average_cpi()