extends Node

@onready var http_settings_container = $"../Camera2D/CanvasLayer/Control/SettingsMenu/ScrollContainer/HTTP_Settings"
@onready var post_button = $"../Camera2D/CanvasLayer/Control/SettingsMenu/HBoxContainer/Button_Post"
@onready var back_to_default_button = $"../Camera2D/CanvasLayer/Control/SettingsMenu/HBoxContainer/Button_Set_Default"

var http_setting_scene = load("res://Nodes/http_setting.tscn")
var settings_json

var config_dictionary = {}

@onready var http_get = $HTTPGet
@onready var http_send = $HTTPSend
@onready var http_retrieve = $HTTPRetrieveDefault

func populate():
    http_send.request("http://127.0.0.1:5000/reset", [], HTTPClient.METHOD_POST)
    
func collect():
    http_send.request("http://127.0.0.1:5000/collect_data", [], HTTPClient.METHOD_POST)


# Called when the node enters the scene tree for the first time.
func _ready():
    post_button.pressed.connect(self._post)
    back_to_default_button.pressed.connect(self._retrieve_default)
    http_get.request_completed.connect(_on_get_request_completed)
    http_send.request_completed.connect(_on_send_request_completed)
    http_retrieve.request_completed.connect(_retrieve_completed)
    save_to_json_button.pressed.connect(_save_as_JSON)
    
    get_config()

func get_config():
    http_get.request("http://127.0.0.1:5000/config")
    
func _on_get_request_completed(_result, response_code, _headers, body):
    if response_code == 200:
        settings_json = JSON.parse_string(body.get_string_from_utf8())
        
        for n in http_settings_container.get_children():
            http_settings_container.remove_child(n)
            n.queue_free()
        
        for conf in settings_json:
            config_dictionary[conf] = http_setting_scene.instantiate()
            http_settings_container.add_child(config_dictionary[conf])
            
            config_dictionary[conf].set_config_name(conf)
            config_dictionary[conf].set_config_value(str(settings_json[conf]))

func _on_send_request_completed(_result, response_code, _headers, _body):
    if response_code == 200:
        print("Send sucess")
        print("Getting results back...")
        http_get.request("http://127.0.0.1:5000/config")
    else:
        print("Code: ", response_code)
          
func _retrieve_default():
    http_retrieve.request(
        "http://127.0.0.1:5000/config", [],
        HTTPClient.METHOD_DELETE
    )

func _retrieve_completed(_result, _response_code, _headers, _body):
    get_config()


@onready var save_to_json_button = $Window/MarginContainer/VBoxContainer/SaveButton
@onready var save_to_json_path_input = $Window/MarginContainer/VBoxContainer/HBoxContainer/LineEdit
func _save_as_JSON():
    for pair in config_dictionary:
        settings_json[pair] = config_dictionary[pair].get_config_value()
    
    var path = "res://"+save_to_json_path_input.text+".json"
    var file = FileAccess.open(path, FileAccess.WRITE)
    file.store_string(JSON.stringify(settings_json))
    
func _post():
    for pair in config_dictionary:
        settings_json[pair] = config_dictionary[pair].get_config_value()
 
    http_send.request(
        "http://127.0.0.1:5000/config", 
        ["Content-Type: application/json"], 
        HTTPClient.METHOD_PATCH, 
        JSON.stringify(settings_json))
