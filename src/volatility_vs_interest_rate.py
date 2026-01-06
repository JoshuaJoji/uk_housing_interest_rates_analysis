import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import os

# Load and merge datasets
def load_and_merge():
    volatility = pd.read_csv(
        "data/processed/yearly_price_volatility.csv"
    )
    rates = pd.read_csv(
        "data/processed/bank_rate_yearly_avg.csv"
    )

    df = pd.merge(volatility, rates, on="Year", how="inner")
    df = df.dropna()

    return df

# Plotting and correlation analysis
def plot_and_correlate(df):
    os.makedirs("outputs", exist_ok=True)

    # Scatter plot
    plt.figure(figsize=(7, 5))
    plt.scatter(
        df["Bank_Rate_Yearly_Avg"],
        df["Price_STD"],
        color="black",
        alpha=0.7,
    )
    plt.xlabel("Bank of England Base Rate (Yearly Avg, %)")
    plt.ylabel("House Price Volatility (Std Dev, £)")
    plt.title("House Price Volatility vs Interest Rate")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("outputs/volatility_vs_interest_rate.png")
    plt.show()

    # Correlation
    r, p = pearsonr(
        df["Bank_Rate_Yearly_Avg"],
        df["Price_STD"],
    )

    print(f"Pearson r: {r:.3f}")
    print(f"p-value: {p:.4f}")


def main():
    df = load_and_merge()
    plot_and_correlate(df)


if __name__ == "__main__":
    main()