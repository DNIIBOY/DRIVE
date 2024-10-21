from flask import Flask, send_from_directory
from valkey import Valkey
from flask_sock import Sock
from simple_websocket.ws import Server
from time import sleep

valkey = Valkey(host="localhost", port=6379, db=0)
sock = Sock()
app = Flask(__name__)
sock.init_app(app)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/set/<name>")
def set_name(name: str):
    valkey.set("name", name)
    return f"<p>Set name to {name}</p>"


@sock.route("/ws")
def socket_test(ws: Server):
    while True:
        name = valkey.get("name")
        ws.send(name)
        sleep(0.2)
