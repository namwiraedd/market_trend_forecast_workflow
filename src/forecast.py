"""
forecast.py
- Loads saved Prophet and LightGBM models and generates a forecast for each saved series.
- Saves CSVs and PNG plots to out_dir.
Usage:
    python src/forecast.py --models_dir models --horizon 12 --out_dir reports
"""
import argparse
import glob
import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

def forecast_prophet(model, periods):
    future = model.make_future_dataframe(periods=periods, freq='MS')
    forecast = model.predict(future)
    return forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(periods)

def forecast_lgb(saved, periods):
    df_feat = saved['feature_df'].copy()
    model = saved['model']
    last = df_feat.iloc[-1:].copy()
    preds = []
    current_date = last['date'].iloc[0]
    for i in range(periods):
        current_date = pd.to_datetime(current_date) + pd.DateOffset(months=1)
        row = last.copy()
        row['month'] = current_date.month
        row['year'] = current_date.year
        X = row.drop(columns=['date','series','value']).values
        yhat = model.predict(X)[0]
        preds.append({'date': current_date, 'yhat': float(yhat)})
        # append to last for iterative forecast
        new_row = row.copy()
        new_row['date'] = current_date
        new_row['value'] = yhat
        last = pd.concat([last, new_row.to_frame().T], ignore_index=True)
    return pd.DataFrame(preds)

def main(models_dir='models', horizon=12, out_dir='reports'):
    os.makedirs(out_dir, exist_ok=True)
    prophet_files = glob.glob(os.path.join(models_dir,'*__prophet.joblib'))
    for pfile in prophet_files:
        base = os.path.splitext(os.path.basename(pfile))[0].replace('__prophet','')
        print('Forecasting', base)
        prop = joblib.load(pfile)
        pf = forecast_prophet(prop, periods=horizon)
        pf.to_csv(os.path.join(out_dir, f'{base}__prophet_forecast.csv'), index=False)
        # corresponding lgb
        lgbp = os.path.join(models_dir, f'{base}__lgb.joblib')
        if os.path.exists(lgbp):
            saved = joblib.load(lgbp)
            lf = forecast_lgb(saved, periods=horizon)
            lf.to_csv(os.path.join(out_dir, f'{base}__lgb_forecast.csv'), index=False)
        # plotting
        try:
            plt.figure(figsize=(8,4))
            plt.plot(pf['ds'], pf['yhat'], label='prophet')
            if os.path.exists(lgbp):
                plt.plot(pd.to_datetime(lf['date']), lf['yhat'], label='lightgbm')
            plt.title(base)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(out_dir, f'{base}_forecast.png'))
            plt.close()
        except Exception as e:
            print('Plot failed', e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--models_dir', default='models')
    parser.add_argument('--horizon', type=int, default=12)
    parser.add_argument('--out_dir', default='reports')
    args = parser.parse_args()
    main(args.models_dir, args.horizon, args.out_dir)
