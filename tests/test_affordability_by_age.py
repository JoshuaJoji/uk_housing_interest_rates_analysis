import pandas as pd


def test_income_dataset_structure():
    df = pd.read_csv("data/raw/Income_by_age_and_gender.csv")
    assert df.shape[1] == 3


def test_affordability_positive():
    income = pd.read_csv("data/raw/Income_by_age_and_gender.csv")
    income.columns = ["Age_Group", "Median_Salary", "Gender"]
    income["Median_Salary"] = pd.to_numeric(income["Median_Salary"], errors="coerce")

    assert (income["Median_Salary"] > 0).all()