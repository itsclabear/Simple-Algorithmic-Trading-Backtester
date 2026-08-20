import backtrader as bt
import yfinance as yf

class SmaCross(bt.Strategy):
    params = (('fast', 10), ('slow', 30),)

    def __init__(self):
        sma1 = bt.indicators.SMA(self.data.close, period=self.params.fast)
        sma2 = bt.indicators.SMA(self.data.close, period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(sma1, sma2)

    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.sell()

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

data_df = yf.download('BBCA.JK', start='2023-01-01', end='2024-01-01', auto_adjust=True, multi_level_index=False)
data_feed = bt.feeds.PandasData(dataname=data_df)
cerebro.adddata(data_feed)

cerebro.broker.setcash(10000000.0) # Modal 10 Juta Rupiah
print(f'Modal Awal: Rp {cerebro.broker.getvalue():,.0f}')
cerebro.run()
print(f'Modal Akhir: Rp {cerebro.broker.getvalue():,.0f}')

# 5. Munculkan Grafik Hasilnya
cerebro.plot(style='candlestick')