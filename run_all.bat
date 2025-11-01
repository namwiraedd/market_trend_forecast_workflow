@echo off
echo === Market Forecast Repo - run_all.bat ===

python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

if not exist data\raw mkdir data\raw
if not exist data\processed mkdir data\processed
if not exist models mkdir models
if not exist reports mkdir reports
if not exist notebooks mkdir notebooks

echo 1) Preprocessing data...
python src\data_processing.py --input_dir data\raw --output_dir data\processed

echo 2) Training models...
python src\train_model.py --data_dir data\processed --models_dir models

echo 3) Evaluate & produce reports...
python src\evaluate.py --data_dir data\processed --models_dir models --out_dir reports

echo 4) Forecast (12 months default)...
python src\forecast.py --models_dir models --horizon 12 --out_dir reports

echo Done. Open dashboard with: streamlit run src/streamlit_app.py
pause
