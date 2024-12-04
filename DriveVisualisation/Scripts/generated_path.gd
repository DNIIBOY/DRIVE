extends Path2D

@export var road_width: SpinBox
@export var road_turn_radius: SpinBox
@export var road_turns: SpinBox
@export var offset = Vector2(0,50)
@export var inoutsize: SpinBox
@export var is_straight: CheckButton
@export var straight_road_length: SpinBox

var road_turn_diameter

@export var input_bake_button: Button

signal baked_road

func _init_bake_road():
    """
    Cleans up before baking road
    """
    road_turn_diameter = road_turn_radius.value * 2
    
    curve.clear_points()
    bake_road()

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    road_turn_diameter = road_turn_radius.value * 2
    input_bake_button.pressed.connect(_init_bake_road)
    bake_road()
    

func bake_road():
    """
    Bakes a road from curves, reads from UI elements.
    """
    if is_straight.is_pressed():
        curve.add_point(Vector2(0,0))
        curve.add_point(Vector2(straight_road_length.value, 0))
    else:
        #The first point, at top left corner
        curve.add_point(Vector2(0,0),
        Vector2(-inoutsize.value,0),
        Vector2(+inoutsize.value,0)) #The first straight line (top left corner to first turn)
        #The second point, at the beginning of the first turn. Right side.
        curve.add_point(
            Vector2(road_width.value+road_turn_radius.value,0),
            Vector2(inoutsize.value,0),
            Vector2(-inoutsize.value,0))    
        
        for i in range(road_turns.value):
            #The point at end of the turn to the right-side turn
            curve.add_point(
                Vector2(road_width.value+road_turn_radius.value, road_turn_diameter * i * 2),
                Vector2(-inoutsize.value,0),
                Vector2(inoutsize.value,0))
            #The point at the beginning of the left-side turn
            curve.add_point(
                Vector2(road_width.value + road_turn_radius.value, road_turn_diameter * (i*2+1)),
                Vector2(inoutsize.value,0),
                Vector2(-inoutsize.value,0))
            #The ponint at the end of the left-side turn
            curve.add_point(
                Vector2(road_turn_radius.value, road_turn_diameter * (i*2+1)),
                Vector2(inoutsize.value,0),
                Vector2(-inoutsize.value,0))
            #the point at the beginning of the right-side turn
            curve.add_point(
                Vector2(road_turn_radius.value, road_turn_diameter * (i*2+2)),
                Vector2(-inoutsize.value,0),
                Vector2(inoutsize.value,0))
        
        # The final straight line, going left to right
        curve.add_point(Vector2(road_width.value + road_turn_diameter, road_turn_diameter * (road_turns.value*2)))
    
    for points in curve.point_count:
        curve.set_point_position(points, curve.get_point_position(points) + offset)
    
    baked_road.emit()
        
    
