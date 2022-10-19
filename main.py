import argparse
import logging
import time
from typing import Dict, Optional, Tuple

from bots import Bot, LimitBot
from emailer import email


def main(instrument: str, base_min: float, target_min: float, debug: bool):
    # TODO(JP): registry + arg
    # bot = GridBot(instrument, base_min, target_min, debug)
    bot = LimitBot(instrument, base_min, target_min, debug)


    """
    # Instead of checking number of orders!
    while True:
        if buy_response_status == "filled" and sell_response_status == "filled":
            buy_response_status, sell_response_status = create_order()
    """

    while True:
        try:
            buy, sell = trade(bot)

            if buy is not None:
                print(f"BUY: {buy}")

                # TODO(JP): bought coin at price
                body = "bought"
                email(subject="BUY FILLED", body=body)

            if sell is not None:
                print(f"SELL: {sell}")

                # TODO(JP): sold coin at price
                body = "sold"
                email(subject="SELL FILLED", body=body)

        except Exception as e:
            trades = bot.get_trades()
            logging.error(f"\tTrades: {trades}")
            logging.error(f"\tError: {e}")

        # TODO(JP): schedule trade() every iter instead of while
        time.sleep(1.0)

    # atexit


def trade(bot: Bot) -> Optional[Tuple[Dict, Dict]]:
    # avoid repeat buy-sell orders for the given instrument
    if bot.num_open_orders > 0:
        return None, None

    # place a buy-sell pair
    buy_response, sell_response = bot.create_order()

    return buy_response, sell_response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--instrument", help="", default="BTC_USDC")
    parser.add_argument("--base-min", help="")
    parser.add_argument("--target-min", help="")
    parser.add_argument("--debug", help="Use UAT instead of Prod", default=False)
    args = parser.parse_args()
    main(args.instrument, args.base_min, args.target_min, args.debug)
