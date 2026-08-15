import sqlite3
import math
from pathlib import Path
from datetime import datetime, timezone


BASE = Path.home() / "GSIS"
DB = BASE / "data/candles.db"


print("==============================")
print("GSIS BACKTEST ENGINE v5.0")
print("==============================")


START_BALANCE = 10000.0
RISK_PERCENT = 1.0

ATR_PERIOD = 14

RR_RATIO = 2.0

MAX_HOLD = 20



def load_candles():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
        SELECT open, high, low, close
        FROM candles
        WHERE symbol='BTCUSDT'
        ORDER BY id ASC
    """)

    data = cur.fetchall()

    conn.close()

    return data



def calculate_atr(candles, period):

    if len(candles) < period + 1:
        return None


    trs = []


    for i in range(1, len(candles)):

        high = candles[i][1]
        low = candles[i][2]
        prev_close = candles[i-1][3]


        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )

        trs.append(tr)


    return sum(trs[-period:]) / period



def ema(values, period):

    if len(values) < period:
        return None


    value = sum(values[:period]) / period

    multiplier = 2 / (period + 1)


    for price in values[period:]:

        value = (
            (price - value)
            *
            multiplier
            +
            value
        )


    return value



def test_trade(direction, candles, index, atr):

    entry = candles[index][3]


    if direction == "LONG":

        stop = entry - atr

        target = entry + (
            atr * RR_RATIO
        )


        for x in range(
            index + 1,
            min(
                index + MAX_HOLD,
                len(candles)
            )
        ):

            high = candles[x][1]
            low = candles[x][2]


            if low <= stop:
                return "LOSS"


            if high >= target:
                return "WIN"



    if direction == "SHORT":

        stop = entry + atr

        target = entry - (
            atr * RR_RATIO
        )


        for x in range(
            index + 1,
            min(
                index + MAX_HOLD,
                len(candles)
            )
        ):

            high = candles[x][1]
            low = candles[x][2]


            if high >= stop:
                return "LOSS"


            if low <= target:
                return "WIN"



    return "LOSS"



def run_backtest():

    candles = load_candles()


    if len(candles) < 200:

        print("INSUFFICIENT DATA")

        return



    closes = [
        c[3]
        for c in candles
    ]


    balance = START_BALANCE


    trades = 0
    wins = 0
    losses = 0


    gross_profit = 0
    gross_loss = 0



    for i in range(
        200,
        len(candles)-MAX_HOLD
    ):


        atr = calculate_atr(
            candles[:i],
            ATR_PERIOD
        )


        if atr is None:
            continue



        ema50 = ema(
            closes[:i],
            50
        )


        ema200 = ema(
            closes[:i],
            200
        )


        if not ema50 or not ema200:
            continue



        direction = None



        if (
            ema50 > ema200
            and closes[i] > ema50
        ):

            direction = "LONG"



        elif (
            ema50 < ema200
            and closes[i] < ema50
        ):

            direction = "SHORT"



        if direction:


            trades += 1


            result = test_trade(
                direction,
                candles,
                i,
                atr
            )


            risk = (
                balance *
                RISK_PERCENT /
                100
            )


            if result == "WIN":

                wins += 1

                balance += (
                    risk *
                    RR_RATIO
                )

                gross_profit += (
                    risk *
                    RR_RATIO
                )


            else:

                losses += 1

                balance -= risk

                gross_loss += risk



    win_rate = 0

    if trades:

        win_rate = round(
            wins / trades * 100,
            2
        )


    profit_factor = 0

    if gross_loss > 0:

        profit_factor = round(
            gross_profit /
            gross_loss,
            2
        )


    net = round(
        (
            balance -
            START_BALANCE
        ),
        2
    )


    print("------------------------------")
    print("GSIS QUANT PERFORMANCE")
    print("------------------------------")


    print({

        "engine":
        "GSIS_BACKTEST_ENGINE_v5.0",

        "candles":
        len(candles),

        "trades":
        trades,

        "wins":
        wins,

        "losses":
        losses,

        "win_rate":
        win_rate,

        "profit_factor":
        profit_factor,

        "starting_balance":
        START_BALANCE,

        "ending_balance":
        round(balance,2),

        "net_profit":
        net,

        "timestamp":
        datetime.now(timezone.utc).isoformat()

    })



if __name__ == "__main__":
    run_backtest()
