import utils
from abc import ABC, abstractmethod
from typing import Dict, Tuple


class Bot(ABC):
    def __init__(
        self,
        instrument_name: str,
        base_min: str,
        target_min: str,
        debug: bool,
    ):
        self.instrument_name = instrument_name
        self.base_min = base_min
        self.target_min = target_min
        self.debug = debug

    def get_open_orders(self) -> Dict:
        # TODO(JP): response_status return
        response_content = utils.post_request(
            method="private/get-open-orders",
            req_id=12,
            params={
                "instrument_name": self.instrument_name,
            },
            debug=self.debug,
        )
        return response_content

    def num_open_orders(self):
        return self.get_open_orders()["result"]["count"]

    def get_trades(self) -> Dict:
        """
        Get trades in event of recovery.
        """
        # TODO(JP): response_status return
        response_content = utils.post_request(
            method="private/get-trades",
            req_id=11,
            params={
                "instrument_name": self.instrument_name,
            },
            debug=self.debug,
        )
        return response_content

    @abstractmethod
    def buy(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def sell(self) -> Dict:
        raise NotImplementedError


class LimitBot(Bot):
    def __init__(
        self,
        instrument_name: str,
        base_min: float,  # budget
        target_min: float,  # budget
        buy_limit: float,
        sell_limit: float
    ):
        super().__init__(
            instrument_name=instrument_name,
            base_min=base_min,
            target_min=target_min,
        )
        self.buy_limit = buy_limit
        self.sell_limit = sell_limit

    # def step(self):
    #     """
    #     Check price
    #     """
    #     if balance_base >= self.base_coin_min and price <= self.buy_limit:
    #         self.buy()
    #
    #     elif balance_target >= self.target_coin_min and price >= self.sell_limit:
    #         self.sell()

    def create_order(self) -> Tuple[Dict, Dict]:
        # create buy order at or below buy_limit price
        buy_response = self.buy()

        # create sell order at or above buy_limit price
        sell_response = self.sell()

        return buy_response, sell_response

    def buy(self) -> Dict:
        """
        From docs
        Helpful information:
        STOP_LIMIT and TAKE_PROFIT_LIMIT will execute a LIMIT order when the trigger_price is reached.
        [x] YES
        STOP_LOSS and TAKE_PROFIT will execute a MARKET order when the trigger_price is reached.
        [] NO

        To create trigger orders against market price:
        trigger_price above market price:
            BUY STOP_LOSS and STOP_LIMIT,
            SELL TAKE_PROFIT and TAKE_PROFIT_LIMIT

        trigger_price below market price:
            SELL STOP_LOSS and STOP_LIMIT,
            BUY TAKE_PROFIT and TAKE_PROFIT_LIMIT

        // Stop Limit Example
        {
           "id": 15,
           "method": "private/create-order",
           "params": {
               "instrument_name": "BTC_USDT",
               "side": "BUY",
               "type": "STOP_LIMIT",
               "quantity": 1,
               "trigger_price": 9000,
               "price": 9100,
               "client_oid": "my_stop_limit_order_0015",
               "time_in_force": "GOOD_TILL_CANCEL"
           },
           "nonce": "1598070206891”
        }
        """

        response_content = utils.post_request(
            method="private/create-order",
            req_id=100,
            params={
                "instrument_name": self.instrument_name,
                "side": "BUY",
                "type": "MARKET",  # TODO(JP)
                # "notional": notional
            },
            debug=self.debug,
        )
        return response_content

    def sell(self) -> Dict:
        response_content = utils.post_request(
            method="private/create-order",
            req_id=101,
            params={
                "instrument_name": self.instrument_name,
                "side": "SELL",
                "type": "MARKET",  # TODO(JP)
                # "notional": notional
            },
            debug=self.debug,
        )
        return response_content

