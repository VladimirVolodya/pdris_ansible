import time
from sys import argv
import requests

from flask import Flask, make_response
import threading

PORT = 8000
TIMEOUT = 5

app = Flask(__name__)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    resp = make_response("Ok\n", 200)
    resp.mimetype = "text/plain"
    return resp


def check_other(ip: str, logfile: str):
    session = requests.Session()
    with open(logfile, "a") as log:
        while True:
            try:
                r = session.get(f"http://{ip}:{PORT}/healthcheck", timeout=1)
                if r.status_code == 200:
                    log.write(f"{ip} is available\n")
                else:
                    log.write(f"{ip} is unavailable\n")
            except requests.ConnectionError as e:
                log.write(str(e) + "\n")
            log.flush()
            time.sleep(TIMEOUT)


if __name__ == "__main__":
    http_thread = threading.Thread(
        target=app.run, kwargs={"host": "0.0.0.0", "port": PORT}
    )
    http_thread.start()
    check_other(argv[1], f"/var/log/{argv[1]}.log")
    http_thread.join()
