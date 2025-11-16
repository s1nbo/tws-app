from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import pandas as pd



class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        self.data: dict[int, pd.DataFrame] = {}


    def historicalData(self, reqId, bar):
        # This method is called repeatedly, once per bar
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

    def historicalDataEnd(self, reqId, start, end):
        print(f"Historical data for reqId {reqId} ended: {start} -> {end}")
        print(self.data[reqId].tail())  # for quick check




app = TradingApp()
app.connect('127.0.0.1', 7497, clientId=0)

# start the network loop
threading.Thread(target=app.run, daemon=True).start()

print("Connected:", app.isConnected())

# define contract
nvda = Contract()
nvda.symbol = "NVDA"
nvda.secType = "STK"
nvda.exchange = "SMART"
nvda.currency = "USD"

# request historical data for NVDA
reqId = 1
app.reqHistoricalData(
    reqId=reqId,
    contract=nvda,
    endDateTime='',
    durationStr='1 D',
    barSizeSetting='1 min',
    whatToShow='TRADES',
    useRTH=1,
    formatDate=1,
    keepUpToDate=False,
    chartOptions=[]
)