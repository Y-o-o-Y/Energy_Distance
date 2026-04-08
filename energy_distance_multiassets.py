import yfinance as yf
import numpy as np
import pandas as pd
import polars as pl
import time
import plotly.graph_objects as go

def fast_abs_diff_sum(arr):
    arr = np.sort(arr)
    n = len(arr)
    return np.sum((2 * np.arange(1, n + 1) - n - 1) * arr) * 2

tickers = ["^GSPC","^RUT", "^IXIC", "^DJI"]

raw_data = yf.download(tickers, start="1995-01-01", interval= '1d')['Close']
log_returns = np.log(raw_data / raw_data.shift(1)).dropna()

df_pl = pl.from_pandas(log_returns.reset_index())

window_size = 30
k_assets = len(tickers)
n_obs = window_size
total_len = len(log_returns)

data_np = log_returns.values
results = np.zeros(total_len - window_size + 1)

start_t = time.time()

for i in range(len(results)):
    window = data_np[i : i + window_size, :]
    s_all = fast_abs_diff_sum(window.ravel())
    s_within_sum = 0
    for j in range(k_assets):
        s_within_sum += fast_abs_diff_sum(window[:, j])
    e_stat = (s_all - k_assets * s_within_sum) / (n_obs**2)
    results[i] = np.sqrt(max(e_stat, 0))

final_dates = log_returns.index[window_size - 1:]
output_df = pd.DataFrame({'Date': final_dates, 'Energy': results})

fig = go.Figure()
fig.add_trace(go.Scatter(x=output_df['Date'], y=output_df['Energy'], name='Energy Distance'))
fig.update_layout(title="Total Energy Distance", template="plotly_dark")
fig.show(renderer="browser")