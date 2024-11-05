extends Camera2D

var pan_value = 3

func _ready() -> void:
    zoom_reset()
    pan_reset()
    
func _input(event):
    if event.is_action("zoom_in"):
        zoom_add(0.1)
    elif event.is_action("zoom_out"):
        zoom_add(-0.1)
    
    if event.is_action("pan_right"):
        pan_horizontal(pan_value)
    elif event.is_action("pan_left"):
        pan_horizontal(-pan_value)
        
    if event.is_action("pan_up"):
        pan_vertical(-pan_value)
    elif event.is_action("pan_down"):
        pan_vertical(pan_value)

func pan_reset() -> void:
    var roadwidth = $"../GeneratedPath".road_width
    var roadradius = $"../GeneratedPath".road_turn_radius
    var roadturns = $"../GeneratedPath".road_turns
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
    set_zoom(currentZoom + Vector2(value, value))
