extends VBoxContainer

var buffer = 20.0
var per_character_width = 8.0

var type
var conf_name

func set_config_name(option_name: String) -> void:
    var pascal_name = option_name.to_pascal_case()
    custom_minimum_size = Vector2(buffer + (per_character_width * pascal_name.length()),0)
    $SettingNameBackground/SettingNameLabel.text = pascal_name
    
func set_config_value(value) -> void:
    if value is int:
        type = "int"
        $SpinBox.value = int(value)
    else:
        type = "float"
        $SpinBox.value = float(value)
    
    
func get_config_value():
    if type == "int":
        return $SpinBox.value
    else:
        return $SpinBox.value

    
