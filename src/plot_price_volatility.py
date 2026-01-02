import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_volatility(
    path="data/processed/yearly_price_volatility.csv",
    out_path="outputs/house_price_volatility_over_time.png",
):
    df = pd.read_csv(path)

    plt.figure(figsize=(10, 5))
    plt.plot(df["Year"], df["Price_STD"], color="black")

    plt.xlabel("Year")
    plt.ylabel("Standard Deviation of Prices (£)")
    plt.title("UK House Price Volatility Over Time")
    plt.grid(True)
    plt.tight_layout()

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.show()


if __name__ == "__main__":
    plot_volatility()