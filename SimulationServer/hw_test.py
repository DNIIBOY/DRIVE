from websockets.sync.client import connect


def show_packet(packet: bytes) -> None:
    val = int.from_bytes(packet, byteorder="big")
    rec_speed = val >> 12
    speed = val & 0xFFF
    print("Recommended speed:", rec_speed)
    print("Speed:", speed)


def main():
    with connect("ws://192.168.4.5/ws/hw/1") as ws:
        pack = None
        latest = pack
        while True:
            command = input("(I)ncrement | (D)ecrement | (B)rake: ").casefold()

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
            elif command == "b":
                val = int(input("Brake pressure: ")) & 0xFF
            else:
                show_packet(latest)

            ws.send(val.to_bytes(2, byteorder="big"))


if __name__ == "__main__":
    main()
