extends Node

var socket = WebSocketPeer.new()

func _ready():
	socket.connect_to_url("localhost")
	
func _process(delta):
	socket.poll()
	if socket.get_ready_state() != WebSocketPeer.State.STATE_OPEN:
		return
	
	socket.get_packet()
	
	while socket.get_available_packet_count():
		print("Got data from server: ", socket.get_packet().to_int32_array())
		
