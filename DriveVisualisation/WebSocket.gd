class_name WebSocketClient
extends Node

@export var handshake_headers: PackedStringArray
@export var supported_protocols: PackedStringArray
var tls_options: TLSOptions = null

var socket := WebSocketPeer.new()
var last_state := WebSocketPeer.STATE_CLOSED

var cars = []

signal connected_to_server()
signal connection_closed()
signal message_received(message: Variant)

const INV_65535 = 1.0 / 65535.0

func remap_to_path_coord(value) -> float:
    return value * INV_65535

func _on_message_received(message: Variant) -> void:
    #$Path2D/CarTest.progress_ratio = remap_to_path_coord(message[0])
    for items in message:
        var car_id = items >> 22 # Shift bits 22 times to the right (Car id to least sig)
        car_id = car_id & 0x3FF # mask the first 10 bits
        
        var car_position = items & 0xFFFF
        
        cars[car_id].progress_ratio = remap_to_path_coord(car_position) #
    
func connect_to_url(url: String) -> int:
    socket.supported_protocols = supported_protocols
    socket.handshake_headers = handshake_headers

    var err := socket.connect_to_url(url, tls_options)
    if err != OK:
        return err

    last_state = socket.get_ready_state()
    return OK


func send(message: String) -> int:
    if typeof(message) == TYPE_STRING:
        return socket.send_text(message)
    return socket.send(var_to_bytes(message))


func get_message() -> Variant:
    if socket.get_available_packet_count() < 1:
        return null
    var pkt := socket.get_packet()
    if socket.was_string_packet():
        return pkt.get_string_from_utf8()
    return pkt.to_int32_array()


func close(code: int = 1000, reason: String = "") -> void:
    socket.close(code, reason)
    last_state = socket.get_ready_state()


func clear() -> void:
    socket = WebSocketPeer.new()
    last_state = socket.get_ready_state()


func get_socket() -> WebSocketPeer:
    return socket


func poll() -> void:
    if socket.get_ready_state() != socket.STATE_CLOSED:
        socket.poll()

    var state := socket.get_ready_state()

    if last_state != state:
        last_state = state
        if state == socket.STATE_OPEN:
            connected_to_server.emit()
        elif state == socket.STATE_CLOSED:
            connection_closed.emit()
    while socket.get_ready_state() == socket.STATE_OPEN and socket.get_available_packet_count():
        message_received.emit(get_message())

var car_scene = load("res://Nodes/Car.tscn")

func _ready() -> void:
    cars.resize(1024)
    for i in range(1024):
        cars[i] = car_scene.instantiate()
        $Path2D.add_child(cars[i])
        
    connect("message_received", Callable(self, "_on_message_received"))
    connect_to_url("ws://localhost:5000/ws")

func _physics_process(_delta: float) -> void:
    poll()
