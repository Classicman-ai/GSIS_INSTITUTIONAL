"""
=========================================================

GSIS INSTITUTIONAL

WEBSOCKET STREAMING ENGINE v1.0

Real-Time Market Feed Layer

=========================================================
"""


import os
import sys
import json
import websocket
from datetime import datetime, UTC


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


if PROJECT_ROOT not in sys.path:

    sys.path.insert(0, PROJECT_ROOT)



from core.event_bus import event_bus



class WebSocketStreamEngine:


    def __init__(self):

        self.symbol = "btcusdt"

        self.url = (
            "wss://stream.binance.com:9443/ws/"
            "btcusdt@trade"
        )

        self.status = "CREATED"





    def process_tick(self, data):


        event = {


            "symbol":

            data["s"],


            "price":

            float(data["p"]),


            "quantity":

            float(data["q"]),


            "time":

            datetime.now(UTC).isoformat()

        }


        print(event)


        event_bus.publish(

            "market_tick",

            event

        )





    def on_message(
            self,
            ws,
            message):


        data = json.loads(message)


        self.process_tick(data)





    def on_error(
            self,
            ws,
            error):


        print(
            "STREAM ERROR:",
            error
        )





    def on_close(
            self,
            ws,
            close_status,
            close_message):


        print(
            "STREAM CLOSED"
        )





    def on_open(
            self,
            ws):


        self.status = "ONLINE"


        print("==============================")
        print("GSIS WEBSOCKET STREAM ONLINE")
        print("==============================")





    def start(self):


        websocket.enableTrace(False)


        ws = websocket.WebSocketApp(

            self.url,

            on_open=self.on_open,

            on_message=self.on_message,

            on_error=self.on_error,

            on_close=self.on_close

        )


        ws.run_forever()





def tick_listener(data):


    print(

        "TICK EVENT RECEIVED:",

        data

    )





if __name__ == "__main__":


    engine = WebSocketStreamEngine()


    event_bus.subscribe(

        "market_tick",

        tick_listener

    )


    engine.start()
