from flask import Flask, send_from_directory
import random
from valkey import Valkey
from flask_sock import Sock
from simple_websocket.ws import Server
from time import sleep
import gevent
from threading import Thread
from car import Car
from driver import Driver

valkey = Valkey(host="localhost", port=6379, db=0)
sock = Sock()
app = Flask(__name__)
sock.init_app(app)


def simulate_val_update():
    """Simulate updating 'val' in valkey every 0.2 seconds."""
    head = Car()
    tail = head

    while True:
        if tail._position > 500:
            tail = Car(next=tail)
            tail.next.prev = tail

        if head._position > 10000:
            tmp = head.prev
            del head
            head = tmp

        car = head
        rep = bytes()
        while car:
            car._position += random.randint(1, 25)
            rep += bytes(car)
            car = car.prev

        valkey.set("cars", rep)
        sleep(0.01)


# Start the background thread to simulate the value update
Thread(target=simulate_val_update, daemon=True).start()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@sock.route("/ws")
def car_socket(ws: Server):
    while True:
        val = valkey.get("cars")
        ws.send(val[::-1])  # Transmission reverses the byte order
        gevent.sleep(0.07)
