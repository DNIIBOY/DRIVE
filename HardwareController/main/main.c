#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "esp_err.h"
#include "nvs_flash.h"
#include "esp_websocket_client.h"
#include "math.h"

#include "wifi.h"
#include "websocket_handler.h"
#include "i2c_handler.h"
#include "HD44780.h"
#include "driver/adc.h"
#include "esp_timer.h"

#define WEBSOCKET_URI "ws://192.168.4.4:5000/ws/hw/2"  // Flask server IP and port

#define ENCODER_DT 19
#define ENCODER_CLK 18

static QueueHandle_t gpio_evt_queue = NULL;  // Updated to QueueHandle_t
static const char *TAG = "main";

uint8_t buffer[2];

// ADC Channel
#define ADC_CHANNEL ADC1_CHANNEL_0

// Interrupt service routine (ISR) for encoder rotation
static void IRAM_ATTR encoder_isr_handler(void *arg) {

    int dt_lvl = gpio_get_level(ENCODER_DT);
    uint16_t direction = (dt_lvl == 0) ? (1 << 14) : (1 << 15);  // Determine rotation direction
    xQueueSendFromISR(gpio_evt_queue, &direction, NULL);         // Send direction to queue
}

// Initialize NVS
void nvs_init(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}

// Encoder Task
void encoder_task(void *param) {
    esp_websocket_client_handle_t client = (esp_websocket_client_handle_t) param;
    uint16_t direction;

    while (true) {
        // Wait for an event from the ISR
        if (xQueueReceive(gpio_evt_queue, &direction, portMAX_DELAY)) {
            buffer[0] = (direction >> 8) & 0xFF;  // High byte
            buffer[1] = direction & 0xFF;         // Low byte

            esp_websocket_client_send_bin(client, (const char*)buffer, sizeof(buffer), portMAX_DELAY);
            ESP_LOGI(TAG, "Encoder rotated, sent value: %d", direction);
        }
    }
}

// Brake Task using legacy ADC driver
//
void braker_task(void *param) {
    int pressure_value;
    int last_brake_pressure_return_value = -1;  // Store the previous pressure value to detect changes
    int brake_pressure_return_value = 0;

    esp_websocket_client_handle_t client = (esp_websocket_client_handle_t)param;

    while (1) {
        // Get raw ADC value from ADC1 channel 0 (GPIO36)
        pressure_value = adc1_get_raw(ADC_CHANNEL);

        // Check if pressure is within the threshold to process further
        if (pressure_value <= 4000) {
            // Calculate the brake pressure as an integer instead of float for efficiency
            int temp = pressure_value - 500;
            temp = temp < 0 ? 0 : temp;  // Clamp to zero if negative
            brake_pressure_return_value = 255 - ((temp * 255) / 3500);  // Scale between 0 and 255
        } else {
            brake_pressure_return_value = 0;
        }

        // Only send data if there is a change in the brake pressure value
        if (brake_pressure_return_value != last_brake_pressure_return_value) {
            uint8_t brake_value = brake_pressure_return_value;
            buffer[0] = brake_value;
            esp_websocket_client_send_bin(client, (const char*)buffer, 1, portMAX_DELAY);
            last_brake_pressure_return_value = brake_pressure_return_value;
            ESP_LOGI(TAG, "Touchsensor pressure: %d%%", (brake_pressure_return_value * 100) / 255);
        }

        // Adjust delay as needed to prevent excessive polling
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
}

// Main application
void app_main(void) {
    // Rotary encoder pin configuration
    gpio_set_direction(ENCODER_CLK, GPIO_MODE_INPUT);
    gpio_set_direction(ENCODER_DT, GPIO_MODE_INPUT);

    // Enable interrupt on rising edge for CLK pin
    gpio_set_pull_mode(ENCODER_CLK, GPIO_PULLDOWN_ENABLE);
    gpio_set_pull_mode(ENCODER_DT, GPIO_PULLDOWN_ENABLE);

    gpio_set_intr_type(ENCODER_CLK, GPIO_INTR_POSEDGE);


    // Create a queue to handle encoder events
    gpio_evt_queue = xQueueCreate(10, sizeof(uint16_t));

    // Install ISR service and attach encoder ISR handler
    gpio_install_isr_service(0);
    gpio_isr_handler_add(ENCODER_CLK, encoder_isr_handler, NULL);

    // Initialize NVS, Wi-Fi, and WebSocket
    nvs_init();               // Initialize NVS
    wifi_init_sta();          // Initialize WiFi
    esp_websocket_client_handle_t client = websocket_init(WEBSOCKET_URI);  // WebSocket client

    // Configure ADC for legacy driver
    adc1_config_width(ADC_WIDTH_BIT_12);  // Set ADC resolution to 12 bits
    adc1_config_channel_atten(ADC_CHANNEL, ADC_ATTEN_DB_0);  // Set ADC attenuation

    // Create tasks
    xTaskCreate(&encoder_task, "Encoder Task", 4096, (void *) client, 4, NULL);
    xTaskCreate(&braker_task, "Brake Task", 2048, (void *) client, 4, NULL);
}
