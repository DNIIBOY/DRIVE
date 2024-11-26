extends Camera2D

var pan_value = 3
@onready var generated_path = $"../GeneratedPath"

func _ready() -> void:
    zoom_reset()
    pan_reset()

var previous_mouse_coord
var current_mouse_coord
var mouse_is_down = false

func _input(event: InputEvent) -> void:
    if event.is_action("zoom_in"):
        #zoom_add(0.1)
        linear_zoom(1.1)
    elif event.is_action("zoom_out"):
        #zoom_add(-0.1)
        linear_zoom(0.9)
    
    if event.is_action("reset_zoom"):
        pan_reset()
        set_zoom(Vector2(1,1))
    #if event.is_action("pan_right"):
        #pan_horizontal(pan_value)
    #elif event.is_action("pan_left"):
        #pan_horizontal(-pan_value)
        #
    #if event.is_action("pan_up"):
        #pan_vertical(-pan_value)
    #elif event.is_action("pan_down"):
        #pan_vertical(pan_value)
    
    """if event.is_action_pressed("click"):
        previous_mouse_coord = get_viewport().get_mouse_position()
        mouse_is_down = true
    elif event.is_action_released("click"):
        mouse_is_down = false"""
        
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
    var roadwidth = generated_path.road_width
    var roadradius = generated_path.road_turn_radius
    var roadturns = generated_path.road_turns
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

func pan_horizontal(value: float) -> void:
    offset = Vector2(offset.x + value, offset.y)

func pan_vertical(value: float) -> void:
    offset = Vector2(offset.x, offset.y + value)

func zoom_add(value: float):
    var currentZoom = get_zoom()
    var targetZoom = currentZoom + Vector2(value, value)
    if targetZoom.y >= 0.5 and targetZoom.x >= 0.5:
        set_zoom(targetZoom)

func linear_zoom(factor: float):
    var target_zoom = get_zoom() * factor
    set_zoom(target_zoom)
    
