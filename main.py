import os

import MetaTrader5 as mt5
from dotenv import load_dotenv
from flask import Flask

from utils import MetaTrader5

# init
load_dotenv()
mt5Id = int(os.getenv('MT5_ID'))
mt5Pass = os.getenv('MT5_PASS')
mt5Server = os.getenv('MT5_SERVER')
symbol = os.getenv('SYMBOL')
minLot = float(os.getenv('MIN_LOT'))
maxLot = float(os.getenv('MAX_LOT'))
slTP = float(os.getenv('SL_TP'))
orderStop = float(os.getenv('ORDER_STOP'))
appName = os.getenv('APP_NAME')

metaTradeInstant = MetaTrader5(
    mt5, mt5Id, mt5Pass, mt5Server, symbol, minLot, maxLot, slTP, orderStop)

app = Flask(appName)


@app.route('/:type')
def trade(type):
    metaTradeInstant.quickTrade(type)
