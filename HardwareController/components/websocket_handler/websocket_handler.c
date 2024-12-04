#include "esp_websocket_client.h" // Include WebSocket client library
#include "esp_log.h"

#include "HD44780.h"

#define WIFI_MAXIMUM_RETRY 10
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1

#define LCD_ADDR 0x27
#define LED_ADDR 0x20

#define SDA_LCD_PIN 7
#define SCL_LCD_PIN 6
#define SDA_LED_PIN 15
#define SCL_LED_PIN 14

#define LCD_COLS 16
#define LCD_ROWS 2

uint16_t current_speed;
uint16_t recommended_speed;

char lcdbuffer_line_1[6];
char lcdbuffer_line_2[6];

static void set_leds(uint8_t led_data) {
    // Write LED data to the I/O expander
    //pcf8574_write(LED_ADDR, led_data);
}

//static EventGroupHandle_t s_wifi_event_group;

static void websocket_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)                                 
{
    esp_websocket_event_data_t *event = (esp_websocket_event_data_t *) event_data;

    switch (event_id) {
        case WEBSOCKET_EVENT_CONNECTED:
            ESP_LOGI("WebSocket_handler", "Connected");
            lcd_init(LCD_ADDR, SDA_LCD_PIN, SCL_LCD_PIN, LCD_COLS, LCD_ROWS);
            lcd_set_cursor(0, 0);
            lcd_write_str("Current:     kmt");

            lcd_set_cursor(0, 1);
            lcd_write_str("Advised:     kmt");

            //pcf8574_init(LED_ADDR, SDA_LED_PIN, SCL_LED_PIN);
            break;

        case WEBSOCKET_EVENT_DISCONNECTED:
            ESP_LOGI("WebSocket_handler", "Disconnected");
            break;

        case WEBSOCKET_EVENT_DATA:
            unsigned int value = 0;
            unsigned char* data = (unsigned char*)event->data_ptr;

            for (int i = 0; i < event->data_len; i++) {
                value = (value << 8) | data[i];  // Combine bytes into an integer
            }

            //ESP_LOGI("WebSocket_handler", "Data received: length=%d, data=0x%08X", event->data_len, value);
            current_speed = (value & 0xFFF) * 0.36;
            recommended_speed = ((value >> 12) & 0xFFF) * 0.36;
            uint8_t LED_data = (value >> 24) & 0xFF;

            sprintf(lcdbuffer_line_1, "%03d", current_speed);  // Ensure 3 digits
            sprintf(lcdbuffer_line_2, "%03d", recommended_speed);  // Ensure 3 digits

            lcd_set_cursor(9, 0);
            lcd_write_str(lcdbuffer_line_1);

            lcd_set_cursor(9, 1);
            lcd_write_str(lcdbuffer_line_2);

            set_leds(LED_data);

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