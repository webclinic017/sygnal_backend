import pandas as pd

from core.indicators.volatility import average_true_range


class SupertrendIndicator():

    def __init__(self, df, period=10, multiplier=3):
        self._df = df
        self._period = period
        self._multiplier = multiplier
        self._calculate()

    def _calculate(self):
        atr = average_true_range(self._df, self._period)
        close = self._df['close']
        hl2 = (self._df['high'] + self._df['low']) / 2
        basic_lowerband = hl2 - (self._multiplier * atr)
        basic_upperband = hl2 + (self._multiplier * atr)

        new_df = pd.DataFrame({
            'close': close,
            'prev_close': close.shift(1),
            'upperband': basic_upperband,
            'prev_upperband': basic_upperband.shift(1),
            'lowerband': basic_lowerband,
            'prev_lowerband': basic_lowerband.shift(1),
            'in_uptrend': False,
        })

        for curr in range(1, len(new_df.index)):
            prev = curr - 1
            if new_df.loc[curr, 'close'] > new_df.loc[prev, 'upperband']:
                new_df.loc[curr, 'in_uptrend'] = True
            elif new_df.loc[curr, 'close'] < new_df.loc[prev, 'lowerband']:
                new_df.loc[curr, 'in_uptrend'] = False
            else:
                new_df.loc[curr, 'in_uptrend'] = new_df.loc[prev, 'in_uptrend']

                if new_df.loc[curr, 'in_uptrend'] and new_df.loc[curr, 'lowerband'] < new_df.loc[prev, 'lowerband']:
                    new_df.loc[curr, 'lowerband'] = new_df.loc[prev, 'lowerband']

                if not new_df.loc[curr, 'in_uptrend'] and new_df.loc[curr, 'upperband'] > new_df.loc[prev, 'upperband']:
                    new_df.loc[curr, 'upperband'] = new_df.loc[prev, 'upperband']

        self._df = new_df

    def supertrend(self) -> pd.Series:
        return self._df['in_uptrend']

    def upper_band(self) -> pd.Series:
        return self._df['upperband']

    def lower_band(self) -> pd.Series:
        return self._df['lowerband']
