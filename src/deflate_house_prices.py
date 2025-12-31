import os
import pandas as pd
import matplotlib.pyplot as plt


def quarter_to_int(q):
    if isinstance(q, str):
        q = q.strip().upper()
        if q.startswith("Q"):
            q = q[1:]
    return int(q)


def load_house_prices(path="data/clean/uk_house_price_quarterly.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Quarter"] = df["Quarter"].apply(quarter_to_int)
    df["UK_Average_House_Price"] = pd.to_numeric(df["UK_Average_House_Price"], errors="coerce")
    df = df.dropna(subset=["Year", "Quarter", "UK_Average_House_Price"]).copy()
    df["Year"] = df["Year"].astype(int)
    df["Quarter"] = df["Quarter"].astype(int)
    return df


def load_cpi_quarterly_avg(path="data/clean/cpi_quarterly_avg.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Quarter"] = df["Quarter"].apply(quarter_to_int)
    df["CPI_Quarterly_Avg"] = pd.to_numeric(df["CPI_Quarterly_Avg"], errors="coerce")
    df = df.dropna(subset=["Year", "Quarter", "CPI_Quarterly_Avg"]).copy()
    df["Year"] = df["Year"].astype(int)
    df["Quarter"] = df["Quarter"].astype(int)
    return df


def merge_house_and_cpi(house: pd.DataFrame, cpi: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(house, cpi, on=["Year", "Quarter"], how="inner")
    df["t"] = df["Year"] * 4 + (df["Quarter"] - 1)
    df = df.sort_values("t").reset_index(drop=True)
    df["Year_Quarter"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
    return df


def deflate_house_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert nominal prices to real prices using CPI.
    Base period CPI = first row of merged dataset.
    Real_Price = Nominal_Price * (CPI_base / CPI_t)
    """
    out = df.copy()
    cpi_base = float(out["CPI_Quarterly_Avg"].iloc[0])
    out["CPI_Base"] = cpi_base
    out["Real_House_Price"] = out["UK_Average_House_Price"] * (cpi_base / out["CPI_Quarterly_Avg"])
    return out


def plot_nominal_vs_real(df: pd.DataFrame, out_path="outputs/nominal_vs_real_house_prices.png") -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    plt.figure(figsize=(12, 5))
    plt.plot(df["t"], df["UK_Average_House_Price"], label="Nominal House Price (£)", color="black")
    plt.plot(df["t"], df["Real_House_Price"], label="Real House Price (CPI-adjusted, base=first quarter)", linestyle="--")
    plt.xlabel("Time (quarters)")
    plt.ylabel("Average House Price (£)")
    plt.title("UK Average House Prices: Nominal vs Real (CPI-adjusted)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()


def main():
    house = load_house_prices()
    cpi = load_cpi_quarterly_avg()
    merged = merge_house_and_cpi(house, cpi)
    merged = deflate_house_prices(merged)
    os.makedirs("data/processed", exist_ok=True)
    merged.to_csv("data/processed/house_prices_with_cpi_real.csv", index=False)
    plot_nominal_vs_real(merged)

    print(merged[["Year", "Quarter", "UK_Average_House_Price", "CPI_Quarterly_Avg", "Real_House_Price"]].head())

if __name__ == "__main__":
    main()