import pandas as pd
import matplotlib.pyplot as plt

def quarter_to_int(q):
    if isinstance(q, str):
        q = q.strip().upper()
        if q.startswith("Q"):
            q = q[1:]
    return int(q)

# -----------------------------
# Load data
# -----------------------------
bank = pd.read_csv("data/clean/bank_rate_quarterly.csv")
house = pd.read_csv("data/clean/uk_house_price_quarterly.csv")

# Clean / type conversion
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
bank = bank.dropna()
house = house.dropna()

# Merge on Year+Quarter
df = pd.merge(bank, house, on=["Year", "Quarter"], how="inner")

# Continuous time variable for sorting
df["t"] = df["Year"] * 4 + (df["Quarter"] - 1)
df = df.sort_values("t").reset_index(drop=True)

df["Year_Quarter"] = df["Year"].astype(int).astype(str) + " Q" + df["Quarter"].astype(int).astype(str)

# -----------------------------
# Plot
# -----------------------------
fig, ax1 = plt.subplots(figsize=(12, 5))

# X-axis positions
x = range(len(df))

# House price on the left axis
ax1.plot(
    x,
    df["UK_Average_House_Price"],
    color="black",
    label="UK Average House Price (£)",
)
ax1.set_xlabel("Year")
ax1.set_ylabel("Average House Price (£)", color="black")
ax1.tick_params(axis="y", labelcolor="black")

# Bank rate on the right axis
ax2 = ax1.twinx()
ax2.plot(
    x,
    df["Bank_Rate_Quarterly_Avg"],
    color="red",
    linestyle="--",
    label="Bank of England Base Rate (%)",
)
ax2.set_ylabel("Base Interest Rate (%)", color="red")
ax2.tick_params(axis="y", labelcolor="red")

year_indices = df.groupby("Year").head(1).index
ax1.set_xticks(year_indices)
ax1.set_xticklabels(df.loc[year_indices, "Year"], rotation=45)

plt.title("UK Average House Prices vs Bank of England Base Rate (Quarterly)")
fig.tight_layout()

#save output
plt.savefig("outputs/house_price_vs_bank_rate_timeline.png")
plt.show()