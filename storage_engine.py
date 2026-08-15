from binance.client import Client
import csv
import os
import time

client = Client()

SYMBOL = "XAUTUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
FILE_NAME = "XAUTUSDT_M1.csv"

print("===================================")
print("GSIS ENGINE 3 - STORAGE ENGINE")
print("===================================")

header = [
    "Open Time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Close Time"
]

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

while True:
    try:

        kline = client.get_klines(
            symbol=SYMBOL,
            interval=INTERVAL,
            limit=1
        )[0]

        row = [
            kline[0],
            kline[1],
            kline[2],
            kline[3],
            kline[4],
            kline[5],
            kline[6]
        ]

        with open(FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print(
            "Saved candle:",
            row[1],
            row[2],
            row[3],
            row[4]
        )

        time.sleep(60)

    except Exception as e:
        print("Storage Error:", e)
        time.sleep(10)
