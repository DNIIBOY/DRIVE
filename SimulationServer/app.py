from flask import Flask, send_from_directory
from valkey import Valkey
from flask_sock import Sock
from simple_websocket.ws import Server
from time import sleep
import gevent

valkey = Valkey(host="localhost", port=6379, db=0)
sock = Sock()
app = Flask(__name__)
sock.init_app(app)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/set/<val>")
def set_name(val: str):
    try:
        val = int(val).to_bytes(length=2, signed=False, byteorder="big")
    except (ValueError, OverflowError):
        return "<p>Value must be an 16 bit unsigned integer</p>", 400

    valkey.set("val", val)
    return f"<p>Set val to {''.join(f'{byte:08b}' for byte in val)}</p>"


@sock.route("/ws")
def socket_test(ws: Server):
    while True:
        val = valkey.get("val")
        ws.send(val[::-1])  # Transmission reverses the byte order
        gevent.sleep(0.2)
