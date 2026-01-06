# Aggregate yearly price volatility from UK housing price paid dataset
import os
print(os.listdir("/Users/joshuajoji/.cache/kagglehub/datasets/hm-land-registry/uk-housing-prices-paid/versions/2"))

# Ensure kagglehub is installed in your environment
import kagglehub

# Download the dataset if not already present
base_path = kagglehub.dataset_download("hm-land-registry/uk-housing-prices-paid")
INPUT_PATH = os.path.join(base_path, "price_paid_records.csv")

# Read and process the dataset in chunks to compute yearly price volatility
import pandas as pd

# Function to aggregate yearly price volatility
def aggregate_yearly_volatility():
    base_path = kagglehub.dataset_download(
        "hm-land-registry/uk-housing-prices-paid"
    )

    input_path = os.path.join(base_path, "price_paid_records.csv")
    output_path = "data/processed/yearly_price_volatility.csv"

    chunksize = 1_000_000
    yearly_prices = {}
# Read the dataset in chunks
    for chunk in pd.read_csv(input_path, chunksize=chunksize):
        chunk["Date of Transfer"] = pd.to_datetime(
            chunk["Date of Transfer"], errors="coerce"
        )
        chunk = chunk.dropna(subset=["Date of Transfer", "Price"])

        chunk["Year"] = chunk["Date of Transfer"].dt.year

        for year, prices in chunk.groupby("Year")["Price"]:
            yearly_prices.setdefault(year, []).extend(prices.values)

    rows = []
    for year, prices in yearly_prices.items():
        rows.append(
            {
                "Year": year,
                "Price_STD": pd.Series(prices).std(),
                "Transaction_Count": len(prices),
            }
        )

    df = pd.DataFrame(rows).sort_values("Year")

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Saved:", output_path)
    print(df.head())


if __name__ == "__main__":
    aggregate_yearly_volatility()