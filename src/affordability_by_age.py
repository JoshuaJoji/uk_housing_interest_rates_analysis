import pandas as pd
import matplotlib.pyplot as plt
import os

# Define file paths
HOUSE_PRICE_PATH = "data/clean/Average_UK_houseprices_and_salary.csv"
INCOME_PATH = "data/raw/Income_by_age_and_gender.csv"

# Load the latest real house price from the CSV file
def load_latest_real_house_price(path=HOUSE_PRICE_PATH) -> float:
    df = pd.read_csv(path)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce") # Convert Year to numeric
    df["Real_House_Price"] = pd.to_numeric(df["Real_House_Price"], errors="coerce") # Convert Real_House_Price to numeric
    df = df.dropna(subset=["Year", "Real_House_Price"]) # Ensure no NaN values
    latest_price = df.sort_values("Year")["Real_House_Price"].iloc[-1]

    return float(latest_price)

# Load income
def load_income_data(path=INCOME_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = ["Age_Group", "Median_Salary", "Gender"]
    df["Median_Salary"] = pd.to_numeric(df["Median_Salary"], errors="coerce") # Convert Median_Salary to numeric
    df = df.dropna(subset=["Median_Salary"])

    return df

# Compute affordability
def compute_affordability(df, house_price):
    df = df.copy()
    df["Years_of_Income_to_Buy"] = house_price / df["Median_Salary"]
    return df

# Plot affordability
def plot_affordability(df, out_path="outputs/affordability_by_age_and_gender.png"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.figure(figsize=(10, 5))

    for gender in df["Gender"].unique():
        subset = df[df["Gender"] == gender]
        plt.plot(
            subset["Age_Group"],
            subset["Years_of_Income_to_Buy"],
            marker="o",
            label=gender,
        )

    plt.xlabel("Age Group")
    plt.ylabel("Years of Income Required")
    plt.title("Housing Affordability by Age Group and Gender")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()

def main():
    house_price = load_latest_real_house_price()
    income = load_income_data()

    affordability = compute_affordability(income, house_price)

    plot_affordability(affordability)

    print("Latest real house price used:", round(house_price, 2))
    print(affordability)

if __name__ == "__main__":
    main()