# Market Forecast Repo

**Turn industry Excel reports into repeatable, interpretable market forecasts.**  
This repo provides a full pipeline: data ingestion → cleaning → model training → forecasting → visualisation.

It was designed for easy handoff: a Python-layman can drop spreadsheets into `data/raw/`, run a single script, and open a dashboard.

---

## Quick summary (2 lines)
1. Put your Excel/CSV reports in `data/raw/`.  
2. Run `./run_all.sh` (Linux/macOS) or `run_all.bat` (Windows).  
3. Open dashboard: `streamlit run src/streamlit_app.py`.

---

## What’s included
- `src/data_processing.py` — loads Excel/CSV files, normalises sheets to `date, series, value`, handles missing values and small gaps.
- `src/train_model.py` — trains **Prophet** (trend/seasonality baseline) and **LightGBM** (feature-based) for each series; saves models to `models/`.
- `src/forecast.py` — generates forecasts for a chosen horizon and outputs CSVs and PNGs under `reports/`.
- `src/evaluate.py` — collates training summary and quick checks.
- `src/streamlit_app.py` — a simple interactive dashboard to view forecasts.
- `notebooks/Market_Forecast_Workflow.ipynb` — step-by-step Jupyter notebook (explanations + runnable cells).
- `requirements.txt` — Python packages.
- `run_all.sh` / `run_all.bat` — one-command pipeline runners.

---

## Installation & Quickstart

### Pre-requirements
- Python 3.8+ (recommended)
- Recommended: 8+ GB RAM
- Optional: `pandoc` if you want PDF export of summaries

### Linux / macOS
```bash
git clone <your-repo-url>
cd <repo>
chmod +x run_all.sh
./run_all.sh
Windows (Command Prompt / PowerShell)
git clone (https://github.com/namwiraedd/market_trend_forecast_workflow.git)
cd <repo>
run_all.bat
What run_all does

Creates (or reuses) a virtual env .venv/

Installs requirements

Runs data processing that converts raw Excel/CSV into data/processed/*.csv

Trains models and saves them to models/

Evaluates and writes outputs into reports/

Tells you how to open the dashboard

How to add new data & re-run

Drop new Excel or CSV files into data/raw/.

Files may contain multiple sheets; each sheet becomes a series.

Re-run ./run_all.sh (or run_all.bat on Windows).

Open streamlit run src/streamlit_app.py to view updated forecasts.

Data expectations & tips

The loader auto-detects date-like columns (e.g., Date, Period, Month).

Prefer consistent periodicity (monthly is recommended). Irregular intervals will be coerced where possible.

If a sheet contains multiple numeric columns, they are converted into separate series automatically.

If your files use non-English month names or unusual date formats, ensure Excel saves them as dates or pre-convert to ISO strings.

Models & methodology (brief)

Prophet — robust baseline for trend and seasonality.

LightGBM — a feature-based regressor using lag/rolling features for improved short-term accuracy.

Forecasts saved as CSVs and plotted PNGs for quick review.

Models are saved as .joblib files for easy reloading.

Deliverables 

Cleaned CSVs in data/processed/

Trained models in models/ (one joblib per series)

Forecasts and charts in reports/

A Jupyter notebook explaining the steps and providing runnable cells

A Streamlit dashboard for interactive viewing

Interpreting accuracy

The reports/training_summary.csv includes LightGBM RMSE per series.

Prophet does not produce RMSE in our simple flow; you can evaluate it by comparing historical holdouts (we can add this on request).

For business-critical deployments, plan for hyperparameter tuning, cross-validation, and more historical data.

Edward Juma -edwardjuma252@gmail.com

requirements.txt

---

# 2) `requirements.txt`
Create file: `requirements.txt`

```text
pandas>=1.3
numpy>=1.21
matplotlib>=3.4
seaborn>=0.11
scikit-learn>=1.0
lightgbm>=3.3
prophet>=1.1
joblib
shap
streamlit
openpyxl
python-dateutil
xlrd
tqdm
plotly
pypandoc
Note: prophet sometimes installs as prophet / cmdstanpy or fbprophet depending on environment. If install issues arise, follow Prophet install docs (it may require pystan or cmdstanpy). For a smooth path on Windows, use conda.
Final notes & run checklist 

Commit all files and push to GitHub.

Drop your spreadsheets into data/raw/. Sheets will be processed into data/processed/.

Run ./run_all.sh (or run_all.bat) — it will create a .venv, install packages, train and produce forecasts.

Open streamlit run src/streamlit_app.py to inspect forecasts interactively.

For handoff, deliver the repo link, a one-paragraph explanation of the intended periodicity, and sample input Excel files.
