"""
train_model.py
- For each CSV in data/processed: train Prophet baseline and LightGBM feature model
- Saves models into models/
Usage:
    python src/train_model.py --data_dir data/processed --models_dir models
"""
import argparse
import os
import glob
import pandas as pd
import numpy as np
import joblib
from prophet import Prophet
import lightgbm as lgb
from sklearn.metrics import mean_squared_error

def make_features(df, lags=(1,3,6,12)):
    df = df.copy().sort_values('date')
    for lag in lags:
        df[f'lag_{lag}'] = df['value'].shift(lag)
    df['rolling_mean_3'] = df['value'].shift(1).rolling(window=3).mean()
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df = df.dropna().reset_index(drop=True)
    return df

def train_lightgbm(df):
    df_feat = make_features(df)
    X = df_feat.drop(columns=['date','series','value'])
    y = df_feat['value']
    split = int(len(X) * 0.8)
    if split < 10:
        raise ValueError("Not enough data for training (need >10 rows)")
    X_train, X_val = X.iloc[:split], X.iloc[split:]
    y_train, y_val = y.iloc[:split], y.iloc[split:]
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
    params = {
        'objective':'regression',
        'metric':'rmse',
        'verbosity':-1,
        'boosting_type':'gbdt',
        'learning_rate':0.05,
        'num_leaves':31
    }
    model = lgb.train(params, train_data, valid_sets=[val_data], num_boost_round=500, early_stopping_rounds=50, verbose_eval=False)
    ypred = model.predict(X_val, num_iteration=model.best_iteration)
    rmse = mean_squared_error(y_val, ypred, squared=False)
    return model, rmse, df_feat

def train_prophet(df):
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    ts = df[['date','value']].rename(columns={'date':'ds','value':'y'})
    m.fit(ts)
    return m

def main(data_dir='data/processed', models_dir='models'):
    os.makedirs(models_dir, exist_ok=True)
    files = glob.glob(os.path.join(data_dir,'*.csv'))
    summary = []
    for f in files:
        try:
            print('Training for', f)
            df = pd.read_csv(f, parse_dates=['date'])
            series_name = os.path.splitext(os.path.basename(f))[0]
            # Prophet
            try:
                prop = train_prophet(df)
                joblib.dump(prop, os.path.join(models_dir, f'{series_name}__prophet.joblib'))
            except Exception as e:
                print('Prophet failed', e)
            # LightGBM
            try:
                lgb_model, rmse, df_feat = train_lightgbm(df)
                joblib.dump({'model':lgb_model, 'feature_df':df_feat}, os.path.join(models_dir, f'{series_name}__lgb.joblib'))
                summary.append({'series':series_name, 'lgb_rmse':rmse})
                print('  LGB RMSE:', round(rmse,4))
            except Exception as e:
                print('LightGBM failed', e)
        except Exception as e:
            print('Failed training for', f, e)
    pd.DataFrame(summary).to_csv(os.path.join(models_dir,'training_summary.csv'), index=False)
    print('Training complete. Models saved to', models_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='data/processed')
    parser.add_argument('--models_dir', default='models')
    args = parser.parse_args()
    main(args.data_dir, args.models_dir)
