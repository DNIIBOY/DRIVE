idf_component_register(SRCS "main.c"
                       INCLUDE_DIRS "."
                       REQUIRES HD44780 i2c_handler websocket_handler esp_websocket_client wifi
                       PRIV_REQUIRES driver nvs_flash)
