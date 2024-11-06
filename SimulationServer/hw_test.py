from websockets.sync.client import connect


def show_packet(packet: bytes) -> None:
    val = int.from_bytes(packet, byteorder="big")
    car_id = val >> 22
    speed = val & 0xFFF
    print("Car ID:", car_id)
    print("Speed:", speed)


def main():
    with connect("ws://localhost:5000/ws/hw/1") as ws:
        pack = None
        latest = pack
        while True:
            command = input("(I)ncrement | (D)ecrement: ").casefold()

            try:
                while True:
                    pack = ws.recv(0.01)
                    if pack is None:
                        latest = pack
                        break
            except TimeoutError:
                latest = pack

            val = 0
            if command == "i":
                val = 1 << 15
            elif command == "d":
                val = 1 << 14
            else:
                show_packet(latest)

            ws.send(val.to_bytes(2, byteorder="big"))


if __name__ == "__main__":
    main()
