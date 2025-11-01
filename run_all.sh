#!/usr/bin/env bash
set -e
echo "=== Market Forecast Repo - run_all.sh ==="

# create venv if missing
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# create necessary folders
mkdir -p data/raw data/processed models reports notebooks

echo "1) Preprocessing data..."
python src/data_processing.py --input_dir data/raw --output_dir data/processed

echo "2) Training models..."
python src/train_model.py --data_dir data/processed --models_dir models

echo "3) Evaluate & produce reports..."
python src/evaluate.py --data_dir data/processed --models_dir models --out_dir reports

echo "4) Forecast (12 months default)..."
python src/forecast.py --models_dir models --horizon 12 --out_dir reports

echo ""
echo "Done. Open dashboard with: streamlit run src/streamlit_app.py"
