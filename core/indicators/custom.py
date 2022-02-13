import pandas as pd
import numpy as np

from ta.momentum import RSIIndicator
from ta.trend import MACD


class RSIMACDCrossIndicator():

    def __init__(
        self,
        close,
        rsi_window=14,
        macd_window_slow=26,
        macd_window_fast=12,
    ):
        self._close = close
        self._rsi_window = rsi_window
        self._macd_window_slow = macd_window_slow
        self._macd_window_fast = macd_window_fast
        self._calculate()

    def _calculate(self):
        rsi_indicator = RSIIndicator(self._close, window=self._rsi_window)
        macd_indicator = MACD(
            self._close,
            window_slow=self._macd_window_slow,
            window_fast=self._macd_window_fast,
        )

        rsi_line = rsi_indicator.rsi()
        macd_line = macd_indicator.macd()
        macd_signal_line = macd_indicator.macd_signal()

        df = pd.DataFrame({
            'rsi_line': rsi_line,
            'macd_line': macd_line,
            'macd_signal_line': macd_signal_line,
        })

        # rsi status
        rsi_conditions = [
            (df['rsi_line'] < 35),
            (df['rsi_line'] >= 35) & (df['rsi_line'] <= 70),
            (df['rsi_line'] > 70),
        ]

        rsi_values = ['undersold', 'neutral', 'overbought']
        df['rsi'] = np.select(rsi_conditions, rsi_values)

        # macd_cross status
        prev_df = df.shift(1)
        macd_conditions = [
            (prev_df['macd_line'] < prev_df['macd_signal_line'])
            & (df['macd_line'] > df['macd_signal_line'])
            & (df['macd_line'] < 0),
        ]

        macd_values = ['macd_cross']
        df['macd'] = np.select(macd_conditions, macd_values, default='neutral')

        # rsi undersold and macd cross
        undersold_cross_conditions = [
            (df['rsi'] == 'undersold') & (df['macd'] == 'macd_cross'),
        ]

        undersold_cross_values = [True]
        df['crossover'] = np.select(
            undersold_cross_conditions,
            undersold_cross_values,
            default=False
        )

        self._df = df

    def rsi(self) -> pd.Series:
        return self._df['rsi']

    def macd(self) -> pd.Series:
        return self._df['macd']

    def macd_signal(self) -> pd.Series:
        return self._df['macd_signal']

    def crossover(self) -> pd.Series:
        return self._df['crossover']

    def is_undersold_and_crossed(self) -> bool:
        rows = self._df['crossover'].tail(2)
        return not rows.iloc[-1] and rows.iloc[0]

    def get_cross_status(self) -> bool:
        status = 'No Cross ❌'
        if self.is_undersold_and_crossed():
            status = 'Crossed ✅'

        return status
