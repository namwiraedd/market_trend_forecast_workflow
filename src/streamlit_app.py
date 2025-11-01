"""
Minimal Streamlit dashboard to load forecast CSVs and show interactive plots.
Run:
    streamlit run src/streamlit_app.py
"""
import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

st.set_page_config(page_title="Market Forecast Dashboard", layout="wide")
st.title('Market Forecast Dashboard')

reports = glob.glob('reports/*__prophet_forecast.csv')
if not reports:
    st.warning("No forecasts found. Run `./run_all.sh` first.")
    st.stop()

options = sorted(list(set([os.path.basename(f).split('__')[0] for f in reports])))
series = st.selectbox('Series', options)

if series:
    pfile = f'reports/{series}__prophet_forecast.csv'
    lfile = f'reports/{series}__lgb_forecast.csv'
    if os.path.exists(pfile):
        pf = pd.read_csv(pfile)
        pf['ds'] = pd.to_datetime(pf['ds'])
        fig = px.line(pf, x='ds', y='yhat', title=f'{series} - Prophet forecast', markers=True)
        st.plotly_chart(fig, use_container_width=True)
        st.write(pf.tail(12))
    else:
        st.write('No Prophet forecast found for this series.')
    if os.path.exists(lfile):
        lf = pd.read_csv(lfile)
        lf['date'] = pd.to_datetime(lf['date'])
        fig2 = px.line(lf, x='date', y='yhat', title=f'{series} - LightGBM forecast', markers=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.write(lf.tail(12))
    else:
        st.write('No LightGBM forecast found for this series.')

st.sidebar.markdown("### Instructions")
st.sidebar.write("Drop Excel/CSV files into `data/raw/` and run `./run_all.sh`.")
