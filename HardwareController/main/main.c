#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "esp_err.h"
#include "nvs_flash.h"
#include "esp_websocket_client.h" // Include WebSocket client library

#include "wifi.h"
#include "websocket_handler.h"

#define WEBSOCKET_URI "ws://192.168.1.68:5000/"  // Replace with your Flask server IP and port

void nvs_init(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}

void app_main(void) {
    // dette er til at gemme SSID og Password
    nvs_init(); // Initialize NVS
    // dette er til at skabe forbindelse ti netværk
    wifi_init_sta(); // Initialize WiFi

    // Initialize GPIO
    gpio_reset_pin(LED_PIN);
    gpio_reset_pin(LED_PIN2);
    gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(LED_PIN2, GPIO_MODE_OUTPUT);

    // Initialize WebSocket client
    esp_websocket_client_handle_t client = websocket_init(WEBSOCKET_URI);

    // Send a test message
    esp_websocket_client_send_text(client, "Hello from ESP32", strlen("Hello from ESP32"), portMAX_DELAY);

    // Keep the WebSocket connection alive
    while (true) {
        vTaskDelay(pdMS_TO_TICKS(1000));
        // Optionally, send more messages or handle other tasks here
        esp_websocket_client_send_text(client, "Hello from ESP32", strlen("Hello from ESP32"), portMAX_DELAY);

    }

    // Cleanup
    esp_websocket_client_stop(client);
    esp_websocket_client_destroy(client);
}
