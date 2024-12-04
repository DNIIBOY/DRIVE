extends Window

@export var activate_button: Button

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    close_requested.connect(_requested_close)
    activate_button.pressed.connect(_requested_open)

func _requested_open():
    if visible == false:
        visible = true
    else:
        visible = false

func _requested_close():
    visible = false
