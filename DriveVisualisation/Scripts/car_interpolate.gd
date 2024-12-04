extends PathFollow2D # Den type node denne script sidder på

var current_progress_ratio = 0.0 # Hvor langt mellem
var target_progress_ratio = 0.0
var interpolate = 0.0
var interpolation_coefficient = 2.3

var car_length_pixel = 394
var car_length_real = 40

func set_car_size(road_pixel_per_dm):
    var desired_pixel_length = road_pixel_per_dm * car_length_real
    var desiredScale = desired_pixel_length / car_length_pixel
    $Sprite2D.scale = Vector2(desiredScale, desiredScale)
    
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
    target_progress_ratio = clamp(target, 0, 1)
    interpolate = 0
        
func _process(delta: float) -> void:
    if active:
        interpolate += delta * interpolation_coefficient
        current_progress_ratio = current_progress_ratio + (target_progress_ratio - current_progress_ratio) * interpolate
        progress_ratio = current_progress_ratio

            
            
