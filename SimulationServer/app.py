from flask import Flask, send_from_directory
from valkey import Valkey
from flask_sock import Sock
from simple_websocket.ws import Server
import gevent
from threading import Thread
from simulation import Simulation
from hardware import decode_hw_packet

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


@sock.route("/ws/vis")
def visulation_socket(ws: Server):
    while True:
        val = valkey.get("cars")
        ws.send(val[::-1])  # Transmission reverses the byte order
        gevent.sleep(0.07)


@sock.route("/ws/hw/<int:hw_id>")
def hardware_socket(ws: Server, hw_id: int):
    print("Connected to hardware:", hw_id)
    while True:
        in_val = ws.receive(timeout=0)
        if in_val:
            car_id, brake_pressure = decode_hw_packet(in_val)
            valkey.set(f"hw{hw_id}_car", car_id)
            valkey.set(f"hw{hw_id}_brake", brake_pressure)
            continue

        gevent.sleep(0.07)
