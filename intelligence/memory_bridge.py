import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from signal_memory_engine import SignalMemoryEngine


class MemoryBridge:


    def __init__(self):

        print("==============================")
        print("GSIS MEMORY BRIDGE v1.0 ONLINE")
        print("==============================")
        print("AUTO SIGNAL STORAGE LINK ACTIVE")
        print("==============================")

        self.memory = SignalMemoryEngine()



    def store_trade_signal(self, result):


        trade_plan = result.get(
            "trade_plan",
            {}
        )


        signal = {

            "symbol":
                trade_plan.get("symbol"),

            "direction":
                trade_plan.get("direction"),

            "entry":
                trade_plan.get("entry"),

            "stop_loss":
                trade_plan.get("stop_loss"),

            "tp1":
                trade_plan.get("tp1"),

            "confidence":
                trade_plan.get(
                    "confidence",
                    0
                ),

            "reasons":
                result.get(
                    "reasons",
                    [
                        "GSIS APPROVED SETUP"
                    ]
                )
        }


        return self.memory.save_signal(signal)



if __name__ == "__main__":


    bridge = MemoryBridge()


    test_signal = {


        "trade_plan": {

            "symbol": "XAUUSD",

            "direction": "SELL",

            "entry": 2387.5,

            "stop_loss": 2387.8,

            "tp1": 2387.2,

            "confidence": 100
        },


        "reasons": [

            "LIQUIDITY SWEEP CONFIRMED",

            "BEARISH FVG",

            "BEARISH CHoCH"

        ]

    }


    result = bridge.store_trade_signal(
        test_signal
    )


    print("==============================")
    print("MEMORY BRIDGE RESULT")
    print("==============================")
    print(result)
