from websockets.sync.client import connect


def main():
    with connect("ws://localhost:5000/ws/hw/1") as ws:
        while True:
            car = int(input("Enter car id: "))
            brake = input("Enter brake pressure: ")

            brake = min(int(brake) if brake else 0, 63)
            val = (car << 6) | brake
            ws.send(val.to_bytes(2, byteorder="big"))


if __name__ == "__main__":
    main()
