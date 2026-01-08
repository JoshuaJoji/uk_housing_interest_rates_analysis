# uk_house_price_analysis

<a href="https://app.circleci.com/pipelines/github/JoshuaJoji/uk_house_price_analysis?branch=main" target="_blank" rel="noopener noreferrer">
  <img src="https://dl.circleci.com/status-badge/img/gh/JoshuaJoji/uk_house_price_analysis/tree/main.svg?style=svg" alt="CircleCI Status">
</a>

This repository contains the datasets, cleaning pipeline, analysis scripts, and unit tests for my DAT5501 project.  
The project explores how UK house prices relate to **inflation (CPI)**, the **Bank of England base rate**, **affordability**, and **market volatility**.

**920 Lines of Code**
---

## Data Sources

Raw datasets are stored in `data/raw/` and cleaned outputs are stored in `data/clean/` and `data/processed/`.

- **UK average house prices (nominal)**: `uk_house_price_annual_average_price.csv`  
  Used to generate a quarterly house price series from 2011 onwards.

- **Bank of England base rate**: `bank_rate.csv`  
  Cleaned and aggregated into quarterly and yearly averages.

- **Consumer Price Index (CPI)**: `CPI_quarterly.csv`  
  Cleaned to quarterly averages and used to deflate nominal house prices into real terms.

- **Real house price + salary dataset**: `Average_UK_houseprices_and_salary.csv`  
  Contains inflation-adjusted house prices and inflation-adjusted median salaries (requires cleaning due to header rows / formatting).

- **Income by age group & gender**: `Income_by_age_and_gender.csv`  
  Used to extend affordability analysis across demographics.

- **HM Land Registry “Price Paid” dataset (large)**  
  Downloaded via `kagglehub` to compute annual house price volatility from transaction-level data.

---

## Cleaning & Processing Pipeline

All cleaning and processing scripts are located in the `src/` directory and are run from the repository root.

### 1) Cleaning scripts (`data/raw` → `data/clean`)

1. `src/clean_house_price_quarterly.py`
   - Reads raw house price file
   - Parses dates and filters from **2011 onwards**
   - Aggregates to quarterly mean
   - Outputs: `data/clean/uk_house_price_quarterly.csv`

2. `src/clean_bank_rate_quarterly.py`
   - Reads raw base rate file
   - Filters from **2011 onwards**
   - Aggregates to quarterly mean
   - Outputs: `data/clean/bank_rate_quarterly.csv`

3. `src/clean_cpi_quarterly.py`
   - Removes non-data rows from CPI file
   - Converts date column and derives Year/Quarter
   - Aggregates to quarterly CPI averages
   - Outputs: `data/clean/cpi_quarterly_avg.csv`

4. `src/clean_real_house_price_salary.py`
   - Removes extra header rows and drops empty columns
   - Standardises schema: `Year`, `Real_House_Price`, `Real_Median_Salary`
   - Outputs: `data/clean/Average_UK_houseprices_and_salary_clean.csv`

---

### 2) Processing / derived datasets (`data/clean` → `data/processed`)

1. `deflate_house_prices.py`
   - Merges quarterly house prices with quarterly CPI
   - Computes **real (CPI-adjusted)** house prices using base CPI = first quarter in series
   - Outputs: `data/processed/house_prices_with_cpi_real.csv`
   - Plot: `outputs/nominal_vs_real_house_prices.png`

2. `aggregate_bank_rate_yearly.py`
   - Aggregates quarterly base rate to yearly average
   - Outputs: `data/processed/bank_rate_yearly_avg.csv`

3. `aggregate_price_paid_volatility.py`
   - Downloads HM Land Registry price paid dataset via `kagglehub`
   - Reads in chunks (memory safe) and computes yearly price dispersion:
     - `Price_STD` = standard deviation of transaction prices per year
     - `Transaction_Count` per year
   - Outputs: `data/processed/yearly_price_volatility.csv`

> Note: the price paid dataset is very large; aggregation should be run locally.  
> CircleCI tests validate the processed output file, not the raw Kaggle download.

---

## Analysis Scripts & Outputs

- `affordability_analysis.py`
  - Computes affordability ratio: `Real_House_Price / Real_Median_Salary`
  - Output plot: `outputs/affordability_ratio_over_time.png`

- `affordability_by_age.py`
  - Uses latest real house price and income by age/gender
  - Computes: `Years_of_Income_to_Buy = House_Price / Median_Salary`
  - Output plot: `outputs/affordability_by_age_and_gender.png`

- `quarterly_changes_analysis.py`
  - Computes quarterly house price % changes
  - Tests Pearson correlation against quarterly base rate
  - Output plot: `outputs/house_price_growth_vs_bank_rate.png`

- `timeline_house_price_vs_bank_rate.py`
  - Dual-axis timeline of quarterly house price vs base rate
  - Output plot: `outputs/house_price_vs_bank_rate_timeline.png`

- `plot_price_volatility.py`
  - Plots annual house price volatility (`Price_STD`) over time
  - Output plot: `outputs/house_price_volatility_over_time.png`

- `volatility_vs_interest_rate.py`
  - Merges annual volatility with yearly base rate averages
  - Produces scatter plot + correlation output
  - Output plot: `outputs/volatility_vs_interest_rate.png`

---

## Unit Tests

Unit tests in `tests/` validate data quality and reproducibility (stable, non-random tests):

- `test_affordability_analysis.py`
  - Required affordability columns exist
  - No missing values in key variables
  - Affordability ratio is valid and > 1
  - Year is integer like and monotonically increasing

- `test_average_uk_houseprices_and_salary.py`
  - Required columns exist
  - Year is integer-like and sorted
  - No missing values in core fields
  - Values are positive and affordability ratio > 1

- `test_affordability_by_age.py`
  - Income dataset has expected 3-column structure
  - Median salary values are numeric and positive
  - Gender categories are valid (Male/Female)

- `test_price_volatility.py`
  - Processed volatility dataset exists and has required columns
  - `Price_STD` and transaction counts are positive
  - Years are ordered correctly

- `test_dataset_sanity.py`
  - Adds CI sanity checks to validate dataset presence, size, and value ranges for reproducible analysis.

Run all tests with:
```bash
pytest -q