import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from src.calculator import add, subtract, multiply, divide

VERSION = os.getenv("APP_VERSION", "v1")
REQUESTS = 0
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUESTS
        path = self.path.split("?")[0]

        if path == "/metrics":
            body = (
                "# HELP calculator_requests_total Non-metrics HTTP requests\n"
                "# TYPE calculator_requests_total counter\n"
                f"calculator_requests_total {REQUESTS}\n"
            )
            content_type = "text/plain; version=0.0.4"
        else:
            REQUESTS += 1
            content_type = "application/json"

            if path == "/health":
                body = json.dumps({"status": "healthy"})
            elif path == "/":
                body = json.dumps({
                    "application": "DevOps Calculator",
                    "version": VERSION,
                    "results": {
                        "add": add(10, 2),
                        "subtract": subtract(10, 2),
                        "multiply": multiply(10, 2),
                        "divide": divide(10, 2),
                    },
                })
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found\n")
                logging.warning("Unknown path requested: %s", path)
                return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        logging.info(format, *args)


if __name__ == "__main__":
    logging.info("Starting calculator version %s on port 8000", VERSION)
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
