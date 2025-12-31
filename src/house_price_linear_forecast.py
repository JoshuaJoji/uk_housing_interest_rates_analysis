import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def quarter_to_int(q):
    if isinstance(q, str):
        q = q.strip().upper()
        if q.startswith("Q"):
            q = q[1:]
    return int(q)


def load_house_price_data(
    path="data/clean/uk_house_price_quarterly.csv",
):
    df = pd.read_csv(path)

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Quarter"] = df["Quarter"].apply(quarter_to_int)
    df["UK_Average_House_Price"] = pd.to_numeric(
        df["UK_Average_House_Price"], errors="coerce"
    )

    df = df.dropna().copy()

    # Continuous quarterly time index
    df["t"] = df["Year"] * 4 + (df["Quarter"] - 1)
    df = df.sort_values("t").reset_index(drop=True)

    return df


def train_test_split_time(df, test_quarters=8):
    train = df.iloc[:-test_quarters]
    test = df.iloc[-test_quarters:]
    return train, test


def fit_linear_model(x, y):
    coeffs = np.polyfit(x, y, deg=1)
    return np.poly1d(coeffs)


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def forecast(model, t_last, n_future=8):
    t_future = np.arange(t_last + 1, t_last + n_future + 1)
    y_future = model(t_future)
    return t_future, y_future


def plot_results(df, train, test, model, t_future, y_future):
    plt.figure(figsize=(10, 5))

    # Actual data
    plt.plot(
        df["t"],
        df["UK_Average_House_Price"],
        label="Actual house prices",
        color="black",
    )

    # Fitted trend (train)
    t_fit = np.linspace(train["t"].min(), t_future.max(), 200)
    plt.plot(
        t_fit,
        model(t_fit),
        linestyle="--",
        label="Linear trend",
    )

    # Forecast
    plt.plot(
        t_future,
        y_future,
        linestyle=":",
        marker="o",
        label="Forecast",
    )

    plt.xlabel("Time (quarters)")
    plt.ylabel("Average House Price (£)")
    plt.title("Linear Trend Forecast of UK Average House Prices")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs("outputs", exist_ok=True)
    plt.savefig("outputs/house_price_linear_forecast.png")
    plt.show()


def main():
    df = load_house_price_data()
    train, test = train_test_split_time(df)

    model = fit_linear_model(
        train["t"].values,
        train["UK_Average_House_Price"].values,
    )

    # Evaluate on test set
    test_preds = model(test["t"].values)
    error = rmse(test["UK_Average_House_Price"].values, test_preds)

    print(f"Test RMSE: £{error:,.0f}")

    # Forecast next 8 quarters
    t_future, y_future = forecast(
        model,
        t_last=df["t"].max(),
        n_future=8,
    )

    plot_results(df, train, test, model, t_future, y_future)


if __name__ == "__main__":
    main()