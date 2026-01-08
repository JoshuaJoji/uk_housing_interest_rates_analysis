import pandas as pd
from pathlib import Path

CLEAN_AFFORDABILITY = Path("data/clean/Average_UK_houseprices_and_salary.csv") # cleaned affordability dataset
HOUSE_PRICES = Path("data/clean/uk_house_price_quarterly.csv") # cleaned house price quarterly dataset
BANK_RATES = Path("data/clean/bank_rate_quarterly.csv") # cleaned bank rate quarterly averages dataset
VOLATILITY = Path("data/processed/yearly_price_volatility.csv") # processed volatility dataset

# Test to ensure the affordability dataset exists and is not empty
def test_clean_affordability_dataset_exists_and_not_empty():
    assert CLEAN_AFFORDABILITY.exists(), "Affordability dataset missing"
    df = pd.read_csv(CLEAN_AFFORDABILITY)
    assert not df.empty, "Affordability dataset is empty"

# Test to ensure the house price quarterly dataset has at least 40 rows
def test_house_price_quarterly_has_minimum_rows():
    df = pd.read_csv(HOUSE_PRICES)
    assert len(df) >= 40, "House price dataset unexpectedly small"

# Test to ensure bank rate quarterly averages are within a valid range
def test_bank_rate_quarterly_has_valid_range():
    df = pd.read_csv(BANK_RATES)
    assert (df["Bank_Rate_Quarterly_Avg"] >= 0).all()
    assert (df["Bank_Rate_Quarterly_Avg"] < 20).all()

# Test to ensure volatility dataset has sufficient history and valid transaction counts
def test_volatility_dataset_has_sufficient_history():
    df = pd.read_csv(VOLATILITY)
    assert len(df) >= 5, "Volatility dataset too short for analysis"
    assert (df["Transaction_Count"] > 0).all()