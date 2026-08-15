import json
import time
import websocket

from data.live.live_market_buffer import update_market

URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"


def connect():
    print("=" * 40)
    print("GSIS BINANCE LIVE DATA ENGINE v2.0")
    print("=" * 40)

    while True:
        ws = None

        try:
            print("Connecting to Binance...")
            ws = websocket.WebSocket()
            ws.connect(URL)

            print("CONNECTED TO BINANCE")
            print("Receiving live BTCUSDT trades...\n")

            while True:
                message = ws.recv()
                trade = json.loads(message)

                market = {
                    "symbol": trade["s"],
                    "price": float(trade["p"]),
                    "quantity": float(trade["q"]),
                    "event_time": trade["E"],
                    "trade_time": trade["T"],
                    "buyer_is_maker": trade["m"],
                    "trade_id": trade["t"]
                }

                update_market(market)

                print(
                    f'BTCUSDT | '
                    f'Price: {market["price"]:.2f} | '
                    f'Qty: {market["quantity"]:.6f}'
                )

        except KeyboardInterrupt:
            print("\nStopping GSIS Live Feed...")
            break

        except Exception as e:
            print(f"\nConnection Lost: {e}")
            print("Reconnecting in 5 seconds...\n")
            time.sleep(5)

        finally:
            try:
                if ws:
                    ws.close()
            except:
                pass


if __name__ == "__main__":
    connect()
