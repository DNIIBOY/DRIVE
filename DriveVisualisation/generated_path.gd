extends Path2D

var road_width = 800
var road_turn_radius = 30
var road_turn_diameter = road_turn_radius * 2
var road_turns = 3
var offset = Vector2(0,0)
var inoutsize = 50



# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    
    """transform.origin = Vector2(
        (road_width + road_turn_diameter) * 0.5,
        road_turn_diameter * road_turn_diameter * 0.5
    )"""
    
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

        
    


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
    pass
