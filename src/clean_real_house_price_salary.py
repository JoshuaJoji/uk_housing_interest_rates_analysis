import pandas as pd
import os


def clean_real_house_price_salary(
    input_path="data/raw/Average_UK_houseprices_and_salary.csv",
    output_path="data/clean/Average_UK_houseprices_and_salary_clean.csv",
):
    # Load raw data
    df = pd.read_csv(input_path)
    df = df.iloc[25:].reset_index(drop=True)


    # Drop columns that are completely empty (common when rows end with a trailing comma)
    df = df.dropna(axis=1, how="all")

    # Strip whitespace from column names
    df.columns = [str(c).strip() for c in df.columns]

    # If it still has more than 3 columns, keep only the first 3
    if df.shape[1] > 3:
        df = df.iloc[:, :3]

    # Now rename to consistent names
    df.columns = ["Year", "Real_House_Price", "Real_Median_Salary"]

    # Convert types (treat 'null' etc as NaN automatically via to_numeric)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["Real_House_Price"] = pd.to_numeric(df["Real_House_Price"], errors="coerce")
    df["Real_Median_Salary"] = pd.to_numeric(df["Real_Median_Salary"], errors="coerce")

    # Drop rows missing year or house price (salary can be missing)
    df = df.dropna(subset=["Year", "Real_House_Price"]).reset_index(drop=True)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("✅ Cleaned successfully")
    print(df.head())
    print("Columns:", list(df.columns))
    print("Shape:", df.shape)


if __name__ == "__main__":
    clean_real_house_price_salary()