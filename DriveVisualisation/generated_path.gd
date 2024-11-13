extends Path2D

var road_width = 800
var road_turn_radius = 30
var road_turn_diameter = road_turn_radius * 2
var road_turns = 3
var offset = Vector2(0,0)
var inoutsize = 50

signal baked_road

@onready var input_road_turn_radius = $"../Camera2D/CanvasLayer/Control/RoadSettings/MarginContainer/VBoxContainer/HBoxContainer/RoadSettingContainer2/RadiusSettingElement2/SpinBox"
@onready var input_road_width = $"../Camera2D/CanvasLayer/Control/RoadSettings/MarginContainer/VBoxContainer/HBoxContainer/RoadSettingContainer/WidthRoadSettingElement/SpinBox"
@onready var input_road_turns = $"../Camera2D/CanvasLayer/Control/RoadSettings/MarginContainer/VBoxContainer/TurnsRoadSettingElement/SpinBox"
@onready var input_bake_button = $"../Camera2D/CanvasLayer/Control/RoadSettings/MarginContainer/VBoxContainer/Button"

func _update_values():
    road_width = input_road_width.value
    road_turn_radius = input_road_turn_radius.value
    road_turn_diameter = road_turn_radius *2
    road_turns = input_road_turns.value
    
    curve.clear_points()
    bake_road()
    baked_road.emit()

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    
    input_bake_button.pressed.connect(_update_values)
    bake_road()
    

func bake_road():
    
    #The first point, at top left corner
    curve.add_point(Vector2(0,0),
    Vector2(-inoutsize,0),
    Vector2(+inoutsize,0)) #The first straight line (top left corner to first turn)
    #The second point, at the beginning of the first turn. Right side.
    curve.add_point(
        Vector2(road_width+road_turn_radius,0),
        Vector2(inoutsize,0),
        Vector2(-inoutsize,0))    
    
    for i in range(road_turns):
        #The point at end of the turn to the right-side turn
        curve.add_point(
            Vector2(road_width+road_turn_radius, road_turn_diameter * i * 2),
            Vector2(-inoutsize,0),
            Vector2(inoutsize,0))
        #The point at the beginning of the left-side turn
        curve.add_point(
            Vector2(road_width + road_turn_radius, road_turn_diameter * (i*2+1)),
            Vector2(inoutsize,0),
            Vector2(-inoutsize,0))
        #The ponint at the end of the left-side turn
        curve.add_point(
            Vector2(road_turn_radius, road_turn_diameter * (i*2+1)),
            Vector2(inoutsize,0),
            Vector2(-inoutsize,0))
        #the point at the beginning of the right-side turn
        curve.add_point(
            Vector2(road_turn_radius, road_turn_diameter * (i*2+2)),
            Vector2(-inoutsize,0),
            Vector2(inoutsize,0))
    
    # The final straight line, going left to right
    curve.add_point(Vector2(road_width + road_turn_diameter, road_turn_diameter * (road_turns*2)))

    print(curve.get_baked_length())
    
