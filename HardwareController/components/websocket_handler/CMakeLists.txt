idf_component_register(SRCS websocket_handler.c
                    INCLUDE_DIRS include
                    REQUIRES esp_websocket_client HD44780 pcf8574)