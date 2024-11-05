from car import Car


def decode_hw_packet(packet: bytes) -> tuple[int, int]:
    """
    Decode a hardware packet.
    :param packet: A 2-byte packet.
    :return: A tuple of the selected car id (0-1023), and the current brake pressure (0-63).
    """
    val = int.from_bytes(packet, byteorder="big")
    car_id = val >> 6
    brake_pressure = val & 0x3F
    return car_id, brake_pressure


def encode_hw_packet(car: Car) -> bytes:
    pass
