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
#include "math.h"

#include "wifi.h"
#include "websocket_handler.h"
#include "i2c_handler.h"
#include "HD44780.h"

#include "driver/adc.h"

#define LCD_ADDR 0x27
#define SDA_PIN 7
#define SCL_PIN 6
#define LCD_COLS 16
#define LCD_ROWS 2

#define WEBSOCKET_URI "ws://192.168.4.5:5000/ws/hw/1"  // Replace with your Flask server IP and port

#define ENCODER_DT 19
#define ENCODER_CLK 18

int CLK_lvl;
int DT_lvl;

uint16_t value;
uint8_t buffer[2];

void nvs_init(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}

void lcd_task(void *param) {
  while (true) {
    lcd_cursor_first_line();
    lcd_write_str("Hello World");
    lcd_set_cursor(0, 1);
    lcd_write_str("Hello world pt2");
    vTaskDelay(2000 / portTICK_PERIOD_MS);
    lcd_cursor_first_line();
    lcd_write_str("WOW");
    lcd_set_cursor(0, 1);
    lcd_write_str("Hello");
  }
}

void encoder_task(void *param) {
    int last_CLK_lvl = gpio_get_level(ENCODER_CLK);
    esp_websocket_client_handle_t client = (esp_websocket_client_handle_t) param;

    while (1) {
        CLK_lvl = gpio_get_level(ENCODER_CLK);
        DT_lvl = gpio_get_level(ENCODER_DT);

        if (last_CLK_lvl == 0 && CLK_lvl == 1) {
            if (DT_lvl == 0) {
                value = (1<<15);
            } else {
                value = (1<<14);
            }

            buffer[0] = (value >> 8) & 0xFF;  // High byte
            buffer[1] = value & 0xFF;         // Low byte

            esp_websocket_client_send_bin(client, (const char*)buffer, sizeof(buffer), portMAX_DELAY);
            vTaskDelay(20 / portTICK_PERIOD_MS);
        }
        last_CLK_lvl = CLK_lvl;
        vTaskDelay(8 / portTICK_PERIOD_MS);
    }
}


void braker_task(void *param) {
  int pressure_value;
  int brake_pressure_return_value = 0;

  esp_websocket_client_handle_t client = (esp_websocket_client_handle_t) param;
  
  while (1) {
    pressure_value = adc1_get_raw(ADC1_CHANNEL_0);
    ESP_LOGI("main: ", "Value: %d", pressure_value);
    if (pressure_value <= 2000) {
      float temp = ((float)pressure_value - 500) / 1500;
      if (temp < 0) {
        temp = 0;
      }
      brake_pressure_return_value = (int)fabs(temp * 255 - 255);
      ESP_LOGI("main: ", "Touchsensor pressure: %d%%", (brake_pressure_return_value * 100 / 255));
    } else {
      brake_pressure_return_value = 0;
    }
    value = brake_pressure_return_value;
    buffer[0] = value; 
    esp_websocket_client_send_bin(client, (const char*)buffer, 1, portMAX_DELAY);
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}



void app_main(void) {

  //Rotary encoder
  gpio_set_direction(ENCODER_CLK, GPIO_MODE_INPUT); 
  gpio_set_direction(ENCODER_DT, GPIO_MODE_INPUT);


    // dette er til at lave i2c linje og lave en lcd_task

    //lcd_init(LCD_ADDR, SDA_PIN, SCL_PIN, LCD_COLS, LCD_ROWS);
    //xTaskCreate(&lcd_task, "Demo Task", 2048, NULL, 5, NULL);

    // dette er til at gemme SSID og Password
    nvs_init(); // Initialize NVS
    // dette er til at skabe forbindelse ti netværk
    wifi_init_sta(); // Initialize WiFi

    // Initialize WebSocket client
    esp_websocket_client_handle_t client = websocket_init(WEBSOCKET_URI);

    // Send a test message
    xTaskCreate(&encoder_task, "Encoder Task", 4096, (void *) client, 4, NULL);
    xTaskCreate(&braker_task, "Demo Task", 2048, (void *) client, 4, NULL);
}

