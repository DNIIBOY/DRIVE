from flask import Flask
from valkey import Valkey

valkey = Valkey(host="localhost", port=6379, db=0)
app = Flask(__name__)


@app.route("/")
def hello_valkey():
    name = valkey.get("name")
    if name:
        name = name.decode()
    return f"<p>Hello, {name}!</p>"


@app.route("/set/<name>")
def set_name(name):
    valkey.set("name", name)
    return f"<p>Set name to {name}</p>"
