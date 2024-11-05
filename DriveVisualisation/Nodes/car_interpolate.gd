extends PathFollow2D

var current_progress_ratio = 0.0
var target_progress_ratio = 0.0
var interpolate = 0.0
var interpolation_coefficient = 2.3

var active = false

func set_inactive():
    active = false
    

func set_new_target(target: float) -> void:
    if active == false or target < 0.001:
        active = true
        current_progress_ratio = target
    target_progress_ratio = target
    interpolate = 0
    
func _process(delta: float) -> void:
    if active:
        interpolate += delta * interpolation_coefficient
        current_progress_ratio = current_progress_ratio + (target_progress_ratio - current_progress_ratio) * interpolate
        progress_ratio = current_progress_ratio
