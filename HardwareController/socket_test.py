from flask import Flask
from flask_sock import Sock
import time
app = Flask(__name__)
sock = Sock(app)


@sock.route('/')
def echo(ws):
    while True:
        data = ws.receive()
        print(data)
        ws.send(data + " recieved on websocket")

if __name__ == '__main__':
    # To run your Flask + WebSocket server in production you can use Gunicorn:
    # gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 module:app
    app.run(host="0.0.0.0", debug=True)
