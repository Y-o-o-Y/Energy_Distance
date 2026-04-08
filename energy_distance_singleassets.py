import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

def fast_sad(x):
    n = len(x)
    x_sorted = np.sort(x)
    return np.sum((2 * np.arange(1, n + 1) - n - 1) * x_sorted) * 2

def optimized_energy_1d(x, y):
    nx, ny = len(x), len(y)
    sad_x = fast_sad(x)
    sad_y = fast_sad(y)
    combined = np.concatenate([x, y])
    sad_combined = fast_sad(combined)
    sad_xy = (sad_combined - sad_x - sad_y) / 2
    
    term1 = 2 * (sad_xy / (nx * ny))
    term2 = sad_x / (nx**2)
    term3 = sad_y / (ny**2)
    return term1 - term2 - term3

tickers = ['MU']
ed_configs = [
    (250, 125, 'Long (250/125)'),
    (120, 60, 'Mid (120/60)'),
    (60, 30, 'Short (60/30)')
]

df_raw = yf.download(tickers, start="2020-01-01")['Close']
df = df_raw.to_frame() if isinstance(df_raw, pd.Series) else df_raw
log_returns = np.log(df / df.shift(1)).dropna()

ed_multiscale = {}
start_t = time.time()

for ticker in tickers:
    rets = log_returns[ticker].values
    for w_size, h_size, label in ed_configs:
        dists = []
        for i in range(len(rets) - w_size + 1):
            window_x = rets[i : i + h_size]
            window_y = rets[i + h_size : i + w_size]
            dists.append(optimized_energy_1d(window_x, window_y))
        ed_multiscale[f"{ticker}_{label}"] = pd.Series(
            dists, index=log_returns.index[w_size-1:]
        ) * 100

fig = go.Figure()
colors = {
    'Long (250/125)': '#636EFA',
    'Mid (120/60)': '#AB63FA',
    'Short (60/30)': '#00CC96'
}

for ticker in tickers:
    for _, _, label in ed_configs:
        key = f"{ticker}_{label}"
        fig.add_trace(go.Scatter(
            x=ed_multiscale[key].index,
            y=ed_multiscale[key],
            name=f"ED {label}",
            line=dict(color=colors[label])
        ))

fig.update_layout(
    height=600,
    template="plotly_dark",
    hovermode="x unified",
    title_text=f"Multi-scale Energy Distance: {tickers[0]}",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.show(renderer="browser")