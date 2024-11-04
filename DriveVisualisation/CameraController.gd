extends Camera2D

var pan_value = 3

func _input(event):
    if event.is_action("zoom_in"):
        zoom(0.1)
    elif event.is_action("zoom_out"):
        zoom(-0.1)
    
    if event.is_action("pan_right"):
        pan_horizontal(pan_value)
    elif event.is_action("pan_left"):
        pan_horizontal(-pan_value)
        
    if event.is_action("pan_up"):
        pan_vertical(-pan_value)
    elif event.is_action("pan_down"):
        pan_vertical(pan_value)
        
    

var focus = false 
func SetFocus(isFocusing: bool) -> void:
    if focus == false:
        focus = true
        pass
    else:
        set_zoom(Vector2(1,1))
        focus = false
      

func pan_horizontal(value: float) -> void:
    offset = Vector2(offset.x + value, offset.y)

func pan_vertical(value: float) -> void:
    offset = Vector2(offset.x, offset.y + value)

func zoom(value: float):
    var currentZoom = get_zoom()
    set_zoom(currentZoom + Vector2(value, value))
