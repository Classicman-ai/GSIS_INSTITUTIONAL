from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timezone

from intelligence.mcp.gsis_mt5_terminal_adapter import adapter


print("==============================")
print("GSIS MT5 BRIDGE SERVER v2.0 ONLINE")
print("METATRADER ADAPTER INTEGRATION ACTIVE")
print("==============================")


HOST = "0.0.0.0"
PORT = 8000


class GSISMT5BridgeHandler(BaseHTTPRequestHandler):

    def send_json(self, data):

        response = json.dumps(data)

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.end_headers()

        self.wfile.write(
            response.encode()
        )


    def do_GET(self):

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()


        if self.path == "/health":

            status = adapter.health()

            self.send_json(
                {
                    "server": "GSIS_MT5_BRIDGE",
                    "status": "ONLINE",
                    "adapter": status,
                    "timestamp": timestamp
                }
            )

            return



        if self.path.startswith("/quote/"):

            symbol = self.path.split("/")[-1]

            quote = adapter.quote(symbol)

            self.send_json(
                {
                    "provider": "MT5_BRIDGE",
                    "symbol": symbol,
                    "quote": quote,
                    "timestamp": timestamp
                }
            )

            return



        if self.path == "/account":

            account = adapter.account()

            self.send_json(
                {
                    "provider": "MT5_BRIDGE",
                    "account": account,
                    "timestamp": timestamp
                }
            )

            return



        self.send_json(
            {
                "status": "UNKNOWN_ENDPOINT",
                "path": self.path,
                "timestamp": timestamp
            }
        )



def run_server():

    server = HTTPServer(
        (HOST, PORT),
        GSISMT5BridgeHandler
    )

    print(
        f"GSIS MT5 BRIDGE LISTENING ON PORT {PORT}"
    )

    server.serve_forever()



if __name__ == "__main__":

    print("==============================")
    print("GSIS MT5 BRIDGE SERVER TEST")
    print("==============================")

    print(adapter.initialize())

    run_server()
