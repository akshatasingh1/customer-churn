# customer-churn

Which contract type should retention efforts prioritize? Kaplan-Meier survival curves and a log-rank test on time-to-churn, segmented by contract type, using the Telco Customer Churn dataset.

See [MEMO.md](MEMO.md) for the finding and recommendation.

## Run it

```
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # .venv/bin/pip on macOS/Linux
.venv/Scripts/python src/survival_analysis.py
```

Outputs:
- Console: segment sample sizes, censoring-balance check, median survival per contract, log-rank test result.
- `outputs/km_curves.png`: all three Kaplan-Meier curves overlaid with confidence-interval bands.

## Data

`data/telco_customer_churn.csv` — Telco Customer Churn (7,043 rows). Relevant columns: `tenure` (duration, months), `Churn` (event indicator), `Contract` (segment: Month-to-month / One year / Two year).
