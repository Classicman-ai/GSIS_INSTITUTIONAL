from binance.client import Client

client = Client()

info = client.get_exchange_info()

found = False

for s in info["symbols"]:
    if "XAU" in s["symbol"]:
        print(s["symbol"])
        found = True

if not found:
    print("No XAU symbol found on Binance Spot")
