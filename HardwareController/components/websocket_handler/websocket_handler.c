#include "esp_websocket_client.h" // Include WebSocket client library
#include "driver/gpio.h"
#include "esp_log.h"

#define LED_PIN2 13

#define WIFI_MAXIMUM_RETRY 10
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1


//static EventGroupHandle_t s_wifi_event_group;

static void websocket_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)                                 
{
    esp_websocket_event_data_t *event = (esp_websocket_event_data_t *) event_data;

    switch (event_id) {
        case WEBSOCKET_EVENT_CONNECTED:
            ESP_LOGI("WebSocket_handler", "Connected");
            gpio_set_level(LED_PIN2, 1);
            break;
        case WEBSOCKET_EVENT_DISCONNECTED:
            ESP_LOGI("WebSocket_handler", "Disconnected");
            gpio_set_level(LED_PIN2, 0);
            break;
        case WEBSOCKET_EVENT_DATA:
            ESP_LOGI("WebSocket_handler", "Data received: length=%d, data=0b%lu", event->data_len, (uint32_t)event->data_ptr);
            break;
        default:
            break;
    }
}

esp_websocket_client_handle_t websocket_init(const char* websocket_uri)
{
    esp_websocket_client_config_t websocket_cfg = {
        .uri = websocket_uri,
    };
    // status led init
    gpio_reset_pin(LED_PIN2);
    gpio_set_direction(LED_PIN2, GPIO_MODE_OUTPUT);
    
    esp_websocket_client_handle_t client = esp_websocket_client_init(&websocket_cfg);
    
    // Register WebSocket events correctly for version 1.2.3
    esp_websocket_register_events(client, WEBSOCKET_EVENT_ANY, websocket_event_handler, client);

    // Connect to WebSocket
    esp_websocket_client_start(client);

    return client;

}