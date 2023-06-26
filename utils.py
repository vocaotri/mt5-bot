class MetaTrader5:
    def __init__(self, mt5, mt5Id, mt5Pass, mt5Server, symbol, minLot, maxLot, slTP, orderStop):
        self.mt5 = mt5
        self.mt5Id = mt5Id
        self.mt5Pass = mt5Pass
        self.mt5Server = mt5Server
        self.symbol = symbol
        self.minLot = minLot
        self.maxLot = maxLot
        self.slTP = slTP
        self.orderStop = orderStop
        hasMT5 = self.mt5.initialize()
        if hasMT5 == False:
            print('MT5 initialize failed, install MT5 and try again')
            quit()
        isLogined = self.mt5.login(self.mt5Id, self.mt5Pass, self.mt5Server)
        if isLogined == False:
            print('Login failed')
            quit()
        myBalance = self.mt5.account_info().balance
        myCurrency = self.mt5.account_info().currency
        if(myCurrency == 'USD' and myBalance >= 100):
            self.minLot = round(self.lotPercent(self.minLot, myBalance), 2)
            self.maxLot = round(self.lotPercent(self.maxLot, myBalance), 2)
        print('MT5 initialize success')

    def market_position(self, typeDirection='buy'):
        action = self.mt5.TRADE_ACTION_DEAL
        type = self.mt5.ORDER_TYPE_BUY
        price = self.mt5.symbol_info_tick(self.symbol).ask
        sl = self.mt5.symbol_info_tick(self.symbol).ask - self.slTP
        tp = self.mt5.symbol_info_tick(self.symbol).ask + self.slTP
        comment = 'Python script open position'
        if typeDirection != 'buy':
            type = self.mt5.ORDER_TYPE_SELL
            price = self.mt5.symbol_info_tick(self.symbol).bid
            sl = self.mt5.symbol_info_tick(self.symbol).bid + self.slTP
            tp = self.mt5.symbol_info_tick(self.symbol).bid - self.slTP

        request = {
            "action": action,
            "symbol": self.symbol,
            "volume": self.minLot,  # FLOAT
            "type": type,
            "price": price,  # FLOAT
            "sl": sl,  # FLOAT,
            "tp": 0.0,  # FLOAT
            "comment": comment,
        }
        position = self.mt5.order_send(request)
        if (position.comment == 'Requote'):
            print('Requote')
            self.market_position(typeDirection)
        return position

    def remove_all_position(self):
        positions = self.mt5.positions_get()
        for position in positions:
            self.mt5.Close(symbol=position.symbol, ticket=position.ticket)

    def order(self, typeDirection='buy'):
        action = self.mt5.TRADE_ACTION_PENDING
        type = self.mt5.ORDER_TYPE_BUY_LIMIT
        price = self.mt5.symbol_info_tick(self.symbol).ask - self.orderStop
        sl = self.mt5.symbol_info_tick(self.symbol).ask - self.slTP
        tp = self.mt5.symbol_info_tick(self.symbol).ask
        comment = 'Python script open order'
        if typeDirection != 'buy':
            type = self.mt5.ORDER_TYPE_SELL_LIMIT
            price = self.mt5.symbol_info_tick(self.symbol).bid + self.orderStop
            sl = self.mt5.symbol_info_tick(self.symbol).bid + self.slTP
            tp = self.mt5.symbol_info_tick(self.symbol).bid

        request = {
            "action": action,
            "symbol": self.symbol,
            "volume": self.maxLot,  # FLOAT
            "type": type,
            "price": price,  # FLOAT
            "sl": sl,  # FLOAT
            "tp": tp,  # FLOAT
            "comment": comment,
        }
        order = self.mt5.order_send(request)
        return order

    def cancel_all_order(self):
        orders = self.mt5.orders_get()
        for order in orders:
            request = {
                "action": self.mt5.TRADE_ACTION_REMOVE,
                "order": order.ticket,  # select the position you want to close
            }
            order = self.mt5.order_send(request)

    def get_account_info(self):
        return self.mt5.account_info()
    
    def lotPercent(self, volume, balance):
        return volume * balance / 100

    def quickTrade(self, typeDirection='buy'):
        self.remove_all_position()
        self.cancel_all_order()
        self.market_position(typeDirection)
        self.order(typeDirection)
