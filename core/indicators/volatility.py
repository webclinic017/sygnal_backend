
import pandas as pd


def average_true_range(df, period=14):
    tr = true_range(df)
    atr = tr.rolling(period).mean()
    return atr


def true_range(df):
    prev_close = df['close'].shift(1)
    high_minus_low = df['high'] - df['low']
    high_minus_prev_close = abs(df['high'] - prev_close)
    low_minus_prev_close = abs(df['low'] - prev_close)
    true_range = pd.DataFrame({
        'high-low': high_minus_low,
        'high-prev_close': high_minus_prev_close,
        'low-prev_close': low_minus_prev_close,
    }).max(axis=1)

    return true_range
