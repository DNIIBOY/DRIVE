#ifndef WEBSOCKET_HANDLER_H
#define WEBSOCKET_HANDLER_H

#include "websocket_handler.c"

// Declare TAG as an external constant so it can be used in `wifi.c`

esp_websocket_client_handle_t websocket_init(const char* websocket_uri);

#endif // WEBSOCKET_HANDLER_H
