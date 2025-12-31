import pandas as pd
import matplotlib.pyplot as plt
import os


def load_affordability_data(
    path="data/clean/Average_UK_houseprices_and_salary.csv",
):
    df = pd.read_csv(path)

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Real_House_Price"] = pd.to_numeric(df["Real_House_Price"], errors="coerce")
    df["Real_Median_Salary"] = pd.to_numeric(df["Real_Median_Salary"], errors="coerce")

    df = df.dropna(subset=["Real_House_Price", "Real_Median_Salary"]).copy()

    return df


def compute_affordability_ratio(df):
    df = df.copy()
    df["Affordability_Ratio"] = (
        df["Real_House_Price"] / df["Real_Median_Salary"])
    return df

def plot_affordability(df, out_path="outputs/affordability_ratio_over_time.png"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(
        df["Year"],
        df["Affordability_Ratio"],
        color="black",
    )

    plt.xlabel("Year")
    plt.ylabel("House Price / Median Salary")
    plt.title("UK Housing Affordability (Real Terms)")
    plt.grid(True)
    years = df["Year"].astype(int)
    plt.xticks(years[::5], years[::5])

    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()


def main():
    df = load_affordability_data()
    df = compute_affordability_ratio(df)

    plot_affordability(df)

    print(df.head())

if __name__ == "__main__":
    main()