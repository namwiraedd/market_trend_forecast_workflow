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
