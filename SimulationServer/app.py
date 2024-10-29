from flask import Flask, send_from_directory
from valkey import Valkey
from flask_sock import Sock
from simple_websocket.ws import Server
import gevent
from threading import Thread
from simulation import Simulation

valkey = Valkey(host="localhost", port=6379, db=0)
sock = Sock()
app = Flask(__name__)
sock.init_app(app)


def simulate_val_update():
    """Simulate updating 'val' in valkey every 0.2 seconds."""
    simulation = Simulation(valkey)
    simulation.main_loop()


Thread(target=simulate_val_update, daemon=True).start()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@sock.route("/test_ws")
def test_socket(ws: Server):
    print("connection")
    val = 1234
    while True:
        ws.send(val.to_bytes(2, "big"))
        print("sending")
        gevent.sleep(0.07)


@sock.route("/ws")
def car_socket(ws: Server):
    while True:
        val = valkey.get("cars")
        ws.send(val[::-1])  # Transmission reverses the byte order
        gevent.sleep(0.07)
