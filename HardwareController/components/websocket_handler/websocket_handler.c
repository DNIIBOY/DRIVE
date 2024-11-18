#include "esp_websocket_client.h" // Include WebSocket client library
#include "esp_log.h"

#include "HD44780.h"

#define WIFI_MAXIMUM_RETRY 10
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1

#define LCD_ADDR 0x27
#define SDA_PIN 7
#define SCL_PIN 6
#define LCD_COLS 16
#define LCD_ROWS 2

uint16_t current_speed;
uint16_t recommended_speed;

char lcdbuffer_line_1[16];
char lcdbuffer_line_2[16];


//static EventGroupHandle_t s_wifi_event_group;

static void websocket_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)                                 
{
    esp_websocket_event_data_t *event = (esp_websocket_event_data_t *) event_data;

    switch (event_id) {
        case WEBSOCKET_EVENT_CONNECTED:
            ESP_LOGI("WebSocket_handler", "Connected");
            lcd_init(LCD_ADDR, SDA_PIN, SCL_PIN, LCD_COLS, LCD_ROWS);
            break;
        case WEBSOCKET_EVENT_DISCONNECTED:
            ESP_LOGI("WebSocket_handler", "Disconnected");
            break;
        case WEBSOCKET_EVENT_DATA:
            uint32_t recieved_data = event->data_ptr;
            ESP_LOGI("WebSocket_handler", "Data received: length=%d, data=0b%lu", event->data_len, recieved_data);
            current_speed = recieved_data & 0xFFF;
            lcd_set_cursor(0, 0);
            sprintf(lcdbuffer_line_1, "CS: %d", current_speed);
            lcd_write_str(lcdbuffer_line_1);
            recommended_speed = (recieved_data >> 12) & 0xFFF;
            lcd_set_cursor(0, 1);
            sprintf(lcdbuffer_line_1, "RS: %d", current_speed);
            lcd_write_str(lcdbuffer_line_2);
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
    
    esp_websocket_client_handle_t client = esp_websocket_client_init(&websocket_cfg);
    
    // Register WebSocket events correctly for version 1.2.3
    esp_websocket_register_events(client, WEBSOCKET_EVENT_ANY, websocket_event_handler, client);

    // Connect to WebSocket
    esp_websocket_client_start(client);

    return client;

}