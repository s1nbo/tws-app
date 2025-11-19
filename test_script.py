import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import config


import threading


class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

class Bot:
    def __init__(self):
        self.api = IBApi()
        self.api.connect(config.host, config.port, clientId=config.client_id)
        threading.Thread(target=self.api.run, daemon=True).start()




b = Bot()