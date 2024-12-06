idf_component_register(SRCS
                    INCLUDE_DIRS "."
                    REQUIRES  HD44780 i2c_handler websocket_handler wifi
                    PRIV_REQUIRES driver nvs_flash
                    )
