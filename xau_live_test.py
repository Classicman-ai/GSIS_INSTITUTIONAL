from binance.client import Client
import time

client = Client()

symbol = "XAUTUSDT"

print("GSIS DATA ENGINE STARTED")
print("Monitoring:", symbol)

while True:
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)

        price = ticker["price"]

        print(
            "XAUTUSDT:",
            price,
            "| Time:",
            time.strftime("%Y-%m-%d %H:%M:%S")
        )

        time.sleep(5)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
