from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw/Income_by_age_and_gender.csv")

def load_income() -> pd.DataFrame:
    assert DATA_PATH.exists(), f"Income dataset not found: {DATA_PATH.resolve()}"
    df = pd.read_csv(DATA_PATH)
    df.columns = [str(c).strip() for c in df.columns]

    if df.shape[1] > 3:
        df = df.iloc[:, :3].copy()

    df.columns = ["Age_Group", "Median_Salary", "Gender"]

    df["Median_Salary"] = pd.to_numeric(df["Median_Salary"], errors="coerce")
    df["Gender"] = df["Gender"].astype(str).str.strip()
    df["Age_Group"] = df["Age_Group"].astype(str).str.strip()

    return df


def test_income_has_expected_shape():
    df = load_income()
    assert df.shape[1] == 3, "Income dataset should have exactly 3 columns"


def test_income_required_columns_non_empty():
    df = load_income()
    assert df["Age_Group"].notna().all(), "Age_Group contains missing values"
    assert df["Gender"].notna().all(), "Gender contains missing values"
    assert df["Median_Salary"].notna().all(), "Median_Salary contains non-numeric/missing values"


def test_income_salaries_positive():
    df = load_income()
    assert (df["Median_Salary"] > 0).all(), "Median_Salary must be positive"


def test_income_has_two_genders():
    df = load_income()
    genders = set(df["Gender"].str.lower().unique())
    assert genders.issubset({"male", "female"}), f"Unexpected gender labels: {genders}"
    assert len(genders) == 3 #force error
#    assert len(genders) == 2, "Expected exactly two genders (Male/Female)"