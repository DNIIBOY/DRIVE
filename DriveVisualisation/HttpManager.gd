extends Node

var http_request_wrapper = preload("res://http_request_wrapper.tscn")
var http_ui_setting_scene = load("res://Nodes/http_setting.tscn")

@export var http_ui_settings_container: HBoxContainer# = $"../Camera2D/CanvasLayer/Control/SettingsMenu/ScrollContainer/HTTP_Settings"

@export var button_patch_config: Button #= $"../Camera2D/CanvasLayer/Control/SettingsMenu/HBoxContainer/Button_Post"
@export var button_retrieve_config: Button #= $"../Camera2D/CanvasLayer/Control/SettingsMenu/HBoxContainer/Button_Set_Default"
@export var button_export_to_json: Button #= $Window/MarginContainer/VBoxContainer/SaveButton
@export var button_import_from_json: Button

@export var save_to_json_path_input: LineEdit #= $Window/MarginContainer/VBoxContainer/HBoxContainer/LineEdit

var config_ui_elements = {}

func _ready():
    button_patch_config.pressed.connect(_patch_config)
    button_retrieve_config.pressed.connect(_retrieve_default)
    button_export_to_json.pressed.connect(_export_as_JSON)
    button_import_from_json.pressed.connect(_import_from_JSON)
    
    get_config()

func instantiate_http_request() -> HTTPRequest:
    var request = http_request_wrapper.instantiate()
    add_child(request)
    return request

func _generic_request_completed(_result, _response_code, _headers, _body, request_instance):
    request_instance.queue_free()
    
func generic_request(endpoint: String, method: HTTPClient.Method):
    var request = instantiate_http_request()
    request.request_completed_wrapper.connect(_generic_request_completed)
    request.request(endpoint, [], method)
    
func get_config():
    var request = instantiate_http_request()
    request.request_completed_wrapper.connect(_on_get_config_completed)
    request.request("http://127.0.0.1:5000/config")
    
func _on_get_config_completed(_result, response_code, _headers, body, request_instance):
    if response_code == 200:
        populate_ui_settings_from_JSON(body.get_string_from_utf8())      
    request_instance.queue_free()
  
func _retrieve_default():
    var request = instantiate_http_request()
    request.request_completed_wrapper.connect(_retrieve_default_completed)
    
    request.request(
        "http://127.0.0.1:5000/config", [],
        HTTPClient.METHOD_DELETE
    )
    
func _retrieve_default_completed(_result, _response_code, _headers, _body, request_instance):
    get_config()
    request_instance.queue_free()
    
func _patch_config():
    var settings = {}
    for pair in config_ui_elements:
        settings[pair] = config_ui_elements[pair].get_config_value()
    
    var request = instantiate_http_request()
    request.request_completed_wrapper.connect(_generic_request_completed)  
    request.request(
        "http://127.0.0.1:5000/config", 
        ["Content-Type: application/json"], 
        HTTPClient.METHOD_PATCH, 
        JSON.stringify(settings))

#region JSON methods
func populate_ui_settings_from_JSON(config_dump: String):
    var settings = JSON.parse_string(config_dump)
    for ui_entry in http_ui_settings_container.get_children():
        http_ui_settings_container.remove_child(ui_entry)
        ui_entry.queue_free()
    
    for entry in settings:
        config_ui_elements[entry] = http_ui_setting_scene.instantiate()
        http_ui_settings_container.add_child(config_ui_elements[entry])
        
        config_ui_elements[entry].set_config_name(entry)
        config_ui_elements[entry].set_config_value(str(settings[entry]))

func _export_as_JSON():
    var settings = {}
    for pair in config_ui_elements:
        settings[pair] = config_ui_elements[pair].get_config_value()
    
    var path = "res://"+save_to_json_path_input.text+".json"
    var file = FileAccess.open(path, FileAccess.WRITE)
    file.store_string(JSON.stringify(settings))
    file.close()

func _import_from_JSON():
    var path = "res://"+save_to_json_path_input.text+".json"
    var file = FileAccess.open(path, FileAccess.READ)
    populate_ui_settings_from_JSON(file.get_as_text())
    file.close()
    _patch_config()
#endregion
    
