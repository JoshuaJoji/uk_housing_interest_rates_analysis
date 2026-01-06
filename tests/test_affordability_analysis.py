import pandas as pd
from pathlib import Path

from affordability_analysis import load_affordability_data, compute_affordability_ratio

DATA_PATH = Path("data/clean/Average_UK_houseprices_and_salary.csv")

# Test cases for affordability_analysis module
def test_input_dataset_exists():
    assert DATA_PATH.exists(), f"Dataset not found at: {DATA_PATH.resolve()}"

# Test loading and cleaning affordability data
def test_load_affordability_data_schema_and_non_empty():
    df = load_affordability_data(str(DATA_PATH))

    expected = {"Year", "Real_House_Price", "Real_Median_Salary"}
    assert expected.issubset(df.columns), f"Missing required columns. Found: {list(df.columns)}"
    assert len(df) > 0, "Dataset is empty after loading/cleaning"

# Additional tests for data integrity and computations
def test_load_affordability_data_no_missing_core_values():
    df = load_affordability_data(str(DATA_PATH))
    core = df[["Year", "Real_House_Price", "Real_Median_Salary"]]
    assert core.notna().all().all(), "Core columns contain NaNs after conversion/dropna"

# Test computation of affordability ratio
def test_compute_affordability_ratio_adds_column_and_valid_values():
    df = load_affordability_data(str(DATA_PATH))
    out = compute_affordability_ratio(df)

    assert "Affordability_Ratio" in out.columns, "Affordability_Ratio column was not created"
    assert out["Affordability_Ratio"].notna().all(), "Affordability_Ratio contains NaNs"
    assert (out["Affordability_Ratio"] > 1).all(), "Affordability_Ratio should be > 1"
    assert (out["Affordability_Ratio"] < 100).all(), (
        "Affordability_Ratio seems unrealistically large; check salary units"
    )

# Test that Year column is integer-like and sorted
def test_year_integer_like_and_sorted():
    df = load_affordability_data(str(DATA_PATH))
    years = pd.to_numeric(df["Year"], errors="coerce")

    assert years.notna().all(), "Year contains non-numeric values"
    assert (years % 1 == 0).all(), "Year contains decimals (should be whole years)"
    assert years.is_monotonic_increasing, "Year should be sorted ascending"