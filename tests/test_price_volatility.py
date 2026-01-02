import pandas as pd


def test_volatility_dataset_exists_and_valid():
    df = pd.read_csv("data/processed/yearly_price_volatility.csv")

    assert {"Year", "Price_STD", "Transaction_Count"}.issubset(df.columns)
    assert (df["Price_STD"] > 0).all()
    assert df["Year"].is_monotonic_increasing
    assert (df["Transaction_Count"] > 0).all()