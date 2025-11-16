from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import pandas as pd
import matplotlib.pyplot as plt
import time


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        self.data: dict[int, pd.DataFrame] = {}


    # Override historicalData method to be used by gethistoricalData
    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = pd.DataFrame(columns=[
                'date', 'open', 'high', 'low', 'close', 'volume'
            ])

        self.data[reqId] = pd.concat([
            self.data[reqId],
            pd.DataFrame([{
                'date':   bar.date,
                'open':   bar.open,
                'high':   bar.high,
                'low':    bar.low,
                'close':  bar.close,
                'volume': bar.volume
            }])
        ], ignore_index=True)
        print(f"Received bar for reqId {reqId}: {bar.date} {bar.close}")

    def historicalDataEnd(self, reqId, start, end):
        print(f"Historical data for reqId {reqId} ended: {start} -> {end}")
        print(self.data[reqId])  # for quick check




app = TradingApp()
app.connect('127.0.0.1', 7497, clientId=0)

# start the network loop
threading.Thread(target=app.run, daemon=True).start()

print("Connected:", app.isConnected())

# define contract
stock = Contract()
stock.symbol = "HOOD"
stock.secType = "STK"
stock.exchange = "SMART"
stock.currency = "USD"

# request historical data for stock
reqId = 1
app.reqHistoricalData(
    reqId=reqId,
    contract=stock,
    endDateTime='20251114 16:00:00',
    durationStr='1 Y',
    barSizeSetting='1 week',
    whatToShow='TRADES',
    useRTH=1,
    formatDate=1,
    keepUpToDate=False,
    chartOptions=[]
)

time.sleep(2)

app.data[reqId].set_index('date')['close'].plot(title='NVDA Historical Close Prices')

plt.show()