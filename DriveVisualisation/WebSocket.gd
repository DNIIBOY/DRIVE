extends Node

var socket = WebSocketPeer.new()

func _ready():
	socket.connect_to_url("localhost:8000/ws")
	
func _process(_delta):
	
	socket.poll()
	if socket.get_ready_state() != WebSocketPeer.State.STATE_OPEN:
		return
	
	
	
	#socket.get_packet()
	var cars = []
	while socket.get_available_packet_count():
		#print("Got data from server: ", socket.get_packet().to_int32_array())
		cars = socket.get_packet().to_int32_array()
	
	#print(cars)
	for car in cars:
		print(car | 4)
	
