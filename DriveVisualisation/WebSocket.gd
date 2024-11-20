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
const INV_16 = 1.0 / 16

var focusedCar = 0
var isFocusing = false
@onready var camera = $Camera2D
@onready var http_manager = $HTTP_Manager

func _input(event):
    if event.is_action_pressed("focus"):
            if isFocusing == false and active_cars.has(focusedCar):
                isFocusing = true
                focus_on_car()
            else:
                isFocusing = false
                camera.get_parent().remove_child(camera)
                self.add_child(camera)
                camera.set_position(Vector2(0,0))
                camera.pan_reset()
                camera.zoom_reset()

func focus_on_car():
    if isFocusing:
        camera.get_parent().remove_child(camera)
        #self.remove_child(camera)
        camera.set_position(Vector2(0,0))
        cars[focusedCar].add_child(camera)
        camera.offset = Vector2(0,0)
        camera.zoom_set(Vector2(2,2))
        

func remap_to_path_coord(value) -> float:
    return value * INV_65535

var active_cars = {}
func _on_message_received(message: Variant) -> void:
    #$Path2D/CarTest.progress_ratio = remap_to_path_coord(message[0])
    var new_active_cars = {}
    for items in message:
        var car_id = items >> 22 # Shift bits 22 times to the right (Car id to least sig)
        new_active_cars[car_id] = true
        
        var car_position = items & 0xFFFF
        var car_coord = remap_to_path_coord(car_position) 

        var is_focused_1 = items & (1 << 16)
        var is_focused_2 = items & (1 << 17)
        
        if is_focused_1 and is_focused_2:
            cars[car_id].modulate = Color.PURPLE
            if focusedCar != car_id:
                focusedCar = car_id
                focus_on_car()
            
            
        elif is_focused_1:
            cars[car_id].modulate = Color.SKY_BLUE
            if focusedCar != car_id:
                focusedCar = car_id
                focus_on_car()
            
            
        elif is_focused_2:
            cars[car_id].modulate = Color.RED
        else:
            var color = items >> 18
            color = color & 0xF
            cars[car_id].modulate = gradient.sample(color * INV_16)
        
        #cars[car_id].progress_ratio = remap_to_path_coord(car_position) #
        cars[car_id].set_new_target(car_coord) #

    for car_ids in active_cars:
        if not new_active_cars.has(car_ids):
            cars[car_ids].set_inactive()
            
    active_cars = new_active_cars
        
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

var gradient = Gradient.new()
@onready var reconnect_button = $Camera2D/CanvasLayer/Control/ReconnectButton
func _ready() -> void:
    $GeneratedPath.baked_road.connect(_bake_visuals)
    reconnect_button.pressed.connect(self._reconnect)
    gradient.set_color(0, Color(1,0,0,1))
    gradient.set_color(1, Color.BLUE)
    gradient.add_point(0.5, Color(0,1,0,1))
        
    
    cars.resize(1024)
    for i in range(1024):
        cars[i] = car_scene.instantiate()
        $GeneratedPath.add_child(cars[i])
    _bake_visuals()
        
    connect("message_received", Callable(self, "_on_message_received"))
    connect_to_url("ws://localhost:5000/ws/vis")

func _reconnect() -> void:
    for car in cars:
        car.set_inactive()
    connect_to_url("ws://localhost:5000/ws/vis")
    http_manager.get_config()

func _physics_process(_delta: float) -> void:
    poll()

var road_width_dm = 50
func _bake_visuals():
    var road_pixel_per_dm = $GeneratedPath.curve.get_baked_length() * INV_65535
    for car in cars:
        car.set_car_size(road_pixel_per_dm)
    var resolution = 30
    var line := $Line2D
    line.clear_points()
    #add_child(line)
    line.default_color = Color.DIM_GRAY
    
    var desired_pixel_length = road_pixel_per_dm * road_width_dm
    line.width = desired_pixel_length
    var samplePoint = 0.0
    
    var inverted_resolution = 1.0 / resolution
    line.add_point($GeneratedPath.curve.sample(0, 0))
    for point in range($GeneratedPath.curve.get_baked_points().size()):
        samplePoint = 0.0
        for subpoint in range(resolution):
            samplePoint += inverted_resolution
            line.add_point($GeneratedPath.curve.sample(point, samplePoint))
            
            
