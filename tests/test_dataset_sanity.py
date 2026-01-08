import pandas as pd
from pathlib import Path

CLEAN_AFFORDABILITY = Path("data/clean/Average_UK_houseprices_and_salary.csv")
HOUSE_PRICES = Path("data/clean/uk_house_price_quarterly.csv")
BANK_RATES = Path("data/clean/bank_rate_quarterly.csv")
VOLATILITY = Path("data/processed/yearly_price_volatility.csv")


def test_clean_affordability_dataset_exists_and_not_empty():
    assert CLEAN_AFFORDABILITY.exists(), "Affordability dataset missing"
    df = pd.read_csv(CLEAN_AFFORDABILITY)
    assert not df.empty, "Affordability dataset is empty"


def test_house_price_quarterly_has_minimum_rows():
    df = pd.read_csv(HOUSE_PRICES)
    assert len(df) >= 40, "House price dataset unexpectedly small"


def test_bank_rate_quarterly_has_valid_range():
    df = pd.read_csv(BANK_RATES)
    assert (df["Bank_Rate_Quarterly_Avg"] >= 0).all()
    assert (df["Bank_Rate_Quarterly_Avg"] < 20).all()


def test_volatility_dataset_has_sufficient_history():
    df = pd.read_csv(VOLATILITY)
    assert len(df) >= 5, "Volatility dataset too short for analysis"
    assert (df["Transaction_Count"] > 0).all()