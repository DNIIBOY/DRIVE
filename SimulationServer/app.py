from flask import Flask, send_from_directory, request
from valkey import Valkey
from flask_sock import Sock
from simple_websocket.ws import Server
import gevent
from threading import Thread
from simulation import Simulation
from config import SimulationConfig

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


@app.route("/config", methods=["GET", "PATCH", "DELETE"])
def config():
    conf = SimulationConfig()

    match request.method:
        case "GET":
            conf.read(valkey)
        case "PATCH":
            data = request.json
            for key, value in data.items():
                if key.startswith("_"):
                    continue
                setattr(conf, key, value)
            conf.save(valkey)
        case "DELETE":
            for key, value in conf.__dict__.items():
                if key.startswith("_"):
                    continue
                valkey.set(key, value)
            conf.read(valkey)

    return conf.to_dict()


@app.route("/reset", methods=["POST"])
def reset():
    valkey.set("reset", 1)
    return "OK"


@app.route("/collect_data", methods=["POST"])
def collect_data():
    valkey.set("collect_data", 1)
    return "OK"


@sock.route("/ws/vis")
def visulation_socket(ws: Server):
    while ws.connected:
        val = valkey.get("cars")
        ws.send(val[::-1])  # Transmission reverses the byte order
        gevent.sleep(0.07)


@sock.route("/ws/hw/<int:hw_id>")
def hardware_socket(ws: Server, hw_id: int):
    print("Connected to hardware:", hw_id)
    while ws.connected:
        in_val = ws.receive(timeout=0)
        if in_val:
            try:
                val = int.from_bytes(in_val, byteorder="big")
            except TypeError:
                print("Not doing anything with this")
                print(in_val)
                continue

            incr = val & (1 << 15)
            decr = val & (1 << 14)
            brake_pressure = val & 0xFFF

            if incr and not decr:
                valkey.incr(f"hw{hw_id}_car")
            elif decr and not incr:
                valkey.decr(f"hw{hw_id}_car")

            valkey.set(f"hw{hw_id}_brake", brake_pressure)
            continue

        head = valkey.get("head")
        tail = valkey.get("tail")
        car_id = valkey.get(f"hw{hw_id}_car")
        rec_speed = valkey.get(f"hw{hw_id}_rec_speed")
        car_speed = valkey.get(f"hw{hw_id}_speed")

        head = int(head.decode()) if head else 0
        tail = int(tail.decode()) if tail else 0
        car_id = int(car_id.decode()) if car_id else 0
        rec_speed = int(rec_speed.decode()) if rec_speed else 0
        car_speed = int(car_speed.decode()) if car_speed else 0

        if car_id < head or car_id > tail:
            car_id = tail
            valkey.set(f"hw{hw_id}_car", car_id)

        rec_speed = car_speed*2
        val = (max(0, rec_speed) << 12) | max(0, car_speed)
        ws.send(val.to_bytes(4, byteorder="big"))
        gevent.sleep(0.2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
