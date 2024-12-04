extends Camera2D

@export var generated_path: Path2D

func _ready() -> void:
    zoom_reset()
    pan_reset()

var previous_mouse_coord
var current_mouse_coord
var mouse_is_down = false

func _input(event: InputEvent) -> void:
    if event.is_action("zoom_in"):
        linear_zoom(1.1)
    elif event.is_action("zoom_out"):
        linear_zoom(0.9)
    
    if event.is_action("reset_zoom"):
        pan_reset()
        set_zoom(Vector2(1,1))
        
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("click"):
        print("Click!")
        previous_mouse_coord = get_viewport().get_mouse_position()
        mouse_is_down = true
    elif event.is_action_released("click"):
        mouse_is_down = false
    
func _process(delta: float) -> void:
    if mouse_is_down:
        current_mouse_coord = get_viewport().get_mouse_position()
        offset += (previous_mouse_coord - current_mouse_coord) / get_zoom()
        previous_mouse_coord = current_mouse_coord

func pan_reset() -> void:
    var roadwidth = generated_path.road_width.value
    var roadradius = generated_path.road_turn_radius.value
    var roadturns = generated_path.road_turns.value
    offset = Vector2(
        (roadwidth + roadradius*2) * 0.5,
        (roadturns * roadradius*2)
    )
    global_position = Vector2(0,0)

func zoom_reset() -> void:
    set_zoom(Vector2(1,1))
    pass
    
func zoom_set(value: Vector2) -> void:
    set_zoom(value)

func zoom_add(value: float):
    var currentZoom = get_zoom()
    var targetZoom = currentZoom + Vector2(value, value)
    if targetZoom.y >= 0.5 and targetZoom.x >= 0.5:
        set_zoom(targetZoom)

func linear_zoom(factor: float):
    var target_zoom = get_zoom() * factor
    set_zoom(target_zoom)
    
