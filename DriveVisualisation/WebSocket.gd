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

var focusedCar = 0
var isFocusing = false
func _input(event):
    if event.is_action_pressed("focus"):
            if isFocusing == false:
                isFocusing = true
                $Camera2D.pan_reset()
                $Camera2D.zoom_set(Vector2(2,2))
            else:
                isFocusing = false
                $Camera2D.global_position = Vector2(0,0)
                $Camera2D.pan_reset()
                $Camera2D.zoom_reset()

func remap_to_path_coord(value) -> float:
    return value * INV_65535

func _on_message_received(message: Variant) -> void:
    #$Path2D/CarTest.progress_ratio = remap_to_path_coord(message[0])
    for items in message:
        var car_id = items >> 22 # Shift bits 22 times to the right (Car id to least sig)
        
        var car_position = items & 0xFFFF
        var car_coord = remap_to_path_coord(car_position) 
        if 0.0 < car_coord:
            cars[car_id].active = true
        
        
        var is_focused_1 = items & (1 << 16)
        var is_focused_2 = items & (1 << 17)
        
        if is_focused_1 and is_focused_2:
            cars[car_id].modulate = Color.PURPLE
            focusedCar = car_id
        elif is_focused_1:
            cars[car_id].modulate = Color.SKY_BLUE
            focusedCar = car_id
        elif is_focused_2:
            cars[car_id].modulate = Color.RED
        else:
            cars[car_id].modulate = Color.GREEN
        
        #cars[car_id].progress_ratio = remap_to_path_coord(car_position) #
        cars[car_id].set_new_target(car_coord) #
    
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
    CreateVisualLine()
    cars.resize(1024)
    for i in range(1024):
        cars[i] = car_scene.instantiate()
        $GeneratedPath.add_child(cars[i])
        
    connect("message_received", Callable(self, "_on_message_received"))
    connect_to_url("ws://localhost:5000/ws/vis")

func _physics_process(_delta: float) -> void:
    poll()
    if(isFocusing):
        $Camera2D.global_position = cars[focusedCar].global_position
        $Camera2D.offset = Vector2(0,0)
    
func CreateVisualLine():
    var resolution = 30
    var line := $Line2D
    #add_child(line)
    line.default_color = Color.DIM_GRAY
    line.width = 35
    var samplePoint = 0.0
    
    """ #Code beneath is for the old path
    var inverted_resolution = 1.0 / resolution
    line.add_point($Path2D.curve.sample(0, 0))
    for point in range($Path2D.curve.get_baked_points().size()):
        samplePoint = 0.0
        for subpoint in range(resolution):
            samplePoint += inverted_resolution
            line.add_point($Path2D.curve.sample(point, samplePoint))
    """
    var inverted_resolution = 1.0 / resolution
    line.add_point($GeneratedPath.curve.sample(0, 0))
    for point in range($GeneratedPath.curve.get_baked_points().size()):
        samplePoint = 0.0
        for subpoint in range(resolution):
            samplePoint += inverted_resolution
            line.add_point($GeneratedPath.curve.sample(point, samplePoint))
            
            
            
