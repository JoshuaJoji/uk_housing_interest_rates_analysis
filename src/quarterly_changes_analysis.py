import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os

# Helper function to convert quarter strings to integers
def quarter_to_int(q):
    if isinstance(q, str):
        q = q.strip().upper()
        if q.startswith("Q"):
            q = q[1:]
    return int(q)

# Load and preprocess data
def load_data(
    bank_path="data/clean/bank_rate_quarterly.csv",
    house_path="data/clean/uk_house_price_quarterly.csv",
):
    bank = pd.read_csv(bank_path)
    house = pd.read_csv(house_path)

    bank["Year"] = pd.to_numeric(bank["Year"], errors="coerce")
    bank["Quarter"] = bank["Quarter"].apply(quarter_to_int)
    bank["Bank_Rate_Quarterly_Avg"] = pd.to_numeric(
        bank["Bank_Rate_Quarterly_Avg"], errors="coerce"
    )

    house["Year"] = pd.to_numeric(house["Year"], errors="coerce")
    house["Quarter"] = house["Quarter"].apply(quarter_to_int)
    house["UK_Average_House_Price"] = pd.to_numeric(
        house["UK_Average_House_Price"], errors="coerce"
    )

    df = pd.merge(bank, house, on=["Year", "Quarter"], how="inner")
    df = df.sort_values(["Year", "Quarter"]).reset_index(drop=True)

    # House price growth only
    df["House_Price_Pct_Change"] = (
        df["UK_Average_House_Price"].pct_change() * 100
    )

    return df.dropna().copy()

# Compute Pearson correlation
def compute_correlation(df):
    r, p = pearsonr(
        df["Bank_Rate_Quarterly_Avg"],
        df["House_Price_Pct_Change"],
    )
    return r, p

# Plot scatter plot
def plot_scatter(df, out_path):
    plt.figure(figsize=(7, 5))
    plt.scatter(
        df["Bank_Rate_Quarterly_Avg"],
        df["House_Price_Pct_Change"],
        alpha=0.7,
        color="black",
    )
    plt.xlabel("Bank of England Base Rate (%)")
    plt.ylabel("Quarterly House Price Change (%)")
    plt.title("House Price Growth vs Bank of England Base Rate")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()


def main():
    df = load_data()
    r, p = compute_correlation(df)

    print(f"Pearson r: {r:.3f}")
    print(f"p-value: {p:.4f}")

    os.makedirs("outputs", exist_ok=True)
    plot_scatter(
        df,
        "outputs/house_price_growth_vs_bank_rate.png",
    )

if __name__ == "__main__":
    main()