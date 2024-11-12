extends PathFollow2D

var current_progress_ratio = 0.0
var target_progress_ratio = 0.0
var interpolate = 0.0
var interpolation_coefficient = 2.3

var active = false

func _ready() -> void:
    $Sprite2D.visible = false

func set_inactive():
    active = false
    $Sprite2D.visible = false
    

func set_new_target(target: float) -> void:
    if active == false:
        active = true
        current_progress_ratio = target
        $Sprite2D.visible = true
    target_progress_ratio = clamp(target, 0.0, 1)
    interpolate = 0
        
func _process(delta: float) -> void:
    if active:
        interpolate += delta * interpolation_coefficient
        current_progress_ratio = current_progress_ratio + (target_progress_ratio - current_progress_ratio) * interpolate
        progress_ratio = current_progress_ratio

            
            
