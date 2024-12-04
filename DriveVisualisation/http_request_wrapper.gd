extends HTTPRequest


signal request_completed_wrapper(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray, request_instance: HTTPRequest)

func _ready() -> void:
    request_completed.connect(_request_completed)

func _request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray):
    request_completed_wrapper.emit(result, response_code, headers, body, self)
