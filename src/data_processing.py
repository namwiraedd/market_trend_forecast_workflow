"""
data_processing.py
- Loads Excel/CSV files from an input directory
- Normalizes sheets to columns: date, series, value
- Handles missing values, small gaps (interpolate), and writes CSVs to output_dir
Usage:
    python src/data_processing.py --input_dir data/raw --output_dir data/processed
"""
import argparse
import os
import glob
import pandas as pd
import numpy as np

def read_excel_all_sheets(path):
    try:
        xls = pd.read_excel(path, sheet_name=None, engine='openpyxl')
    except Exception:
        xls = pd.read_excel(path, sheet_name=None)
    return xls

def standardize_df(df):
    df = df.copy()
    # try to find a date column
    date_cols = [c for c in df.columns if 'date' in c.lower() or 'month' in c.lower() or 'period' in c.lower()]
    if date_cols:
        date_col = date_cols[0]
    else:
        # fallback: first column
        date_col = df.columns[0]
    df = df.rename(columns={date_col: 'date'})
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # numeric columns
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num_cols:
        # try coercion
        for c in df.columns:
            if c != 'date':
                df[c] = pd.to_numeric(df[c], errors='coerce')
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) > 1:
        df = df.melt(id_vars=['date'], value_vars=num_cols, var_name='series', value_name='value')
    else:
        # pick second column if available
        val_col = num_cols[0] if num_cols else (df.columns[1] if len(df.columns)>1 else None)
        if val_col is None:
            raise ValueError("No numeric column found")
        df = df.rename(columns={val_col: 'value'})
        df['series'] = df.get('series', 'series_1')
    df = df.dropna(subset=['date'])
    df = df.sort_values('date')
    # interpolate small gaps and forward/backfill
    df['value'] = df['value'].interpolate(method='linear', limit=3).fillna(method='ffill').fillna(method='bfill')
    return df[['date','series','value']]

def process_all(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = []
    for ext in ('xls','xlsx','csv'):
        files.extend(glob.glob(os.path.join(input_dir, f'*.{ext}')))
    if not files:
        print('No data files found in', input_dir)
        return
    for p in files:
        print('Reading', p)
        base = os.path.splitext(os.path.basename(p))[0]
        if p.lower().endswith('.csv'):
            # read as single sheet
            try:
                df = pd.read_csv(p)
                try:
                    sdf = standardize_df(df)
                    out_path = os.path.join(output_dir, f"{base}__sheet1.csv")
                    sdf.to_csv(out_path, index=False)
                    print('  -> wrote', out_path)
                except Exception as e:
                    print('  Skip CSV', p, e)
            except Exception as e:
                print('  Failed to read CSV', p, e)
            continue
        try:
            sheets = read_excel_all_sheets(p)
            for name, df in sheets.items():
                try:
                    sdf = standardize_df(df)
                    safe_name = f"{base}__{name}.csv".replace(' ','_')
                    out_path = os.path.join(output_dir, safe_name)
                    sdf.to_csv(out_path, index=False)
                    print('  -> wrote', out_path)
                except Exception as e:
                    print('  Skipped sheet', name, 'due to', e)
        except Exception as e:
            print('Failed to read', p, e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', default='data/raw')
    parser.add_argument('--output_dir', default='data/processed')
    args = parser.parse_args()
    process_all(args.input_dir, args.output_dir)
