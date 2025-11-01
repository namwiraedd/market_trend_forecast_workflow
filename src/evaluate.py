"""
evaluate.py
- Collects files like training_summary.csv and writes them to reports/
- Minimal step for handoff; extend as needed
"""
import argparse
import os
import glob
import pandas as pd
import shutil

def main(data_dir='data/processed', models_dir='models', out_dir='reports'):
    os.makedirs(out_dir, exist_ok=True)
    ts = os.path.join(models_dir,'training_summary.csv')
    if os.path.exists(ts):
        shutil.copy2(ts, os.path.join(out_dir,'training_summary.csv'))
        print('Copied training_summary.csv to reports')
    else:
        print('No training_summary.csv found in models/')
    # list forecasts
    fcs = glob.glob(os.path.join(out_dir,'*_forecast.csv'))
    print('Found forecasts:', fcs)
    print('Evaluation complete.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='data/processed')
    parser.add_argument('--models_dir', default='models')
    parser.add_argument('--out_dir', default='reports')
    args = parser.parse_args()
    main(args.data_dir, args.models_dir, args.out_dir)
