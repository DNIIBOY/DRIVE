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
#define SDA_PIN 4
#define SCL_PIN 5
#define LCD_COLS 16
#define LCD_ROWS 2

#define WEBSOCKET_URI "ws://192.168.1.68:5000/"  // Replace with your Flask server IP and port

#define LED_PIN 12 // onboard led
#define LED_PIN2 13 // onboard led

#define ENCODER_DT 19
#define ENCODER_CLK 18

int adc_value_x;
int adc_value_y;

uint16_t car_id = 0;
int CLK_lvl;
int DT_lvl;

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
while (1) {
    CLK_lvl = gpio_get_level(ENCODER_CLK);
    DT_lvl = gpio_get_level(ENCODER_DT);

    if (last_CLK_lvl == 0 && CLK_lvl == 1) {
      if (DT_lvl == 0) {
        if (car_id != 0)
        car_id--;
      } else {
        car_id++;
      }
      ESP_LOGI("main:", "%d", car_id);
      vTaskDelay(20 / portTICK_PERIOD_MS);
    }
    last_CLK_lvl = CLK_lvl;
    vTaskDelay(8 / portTICK_PERIOD_MS);
  }
}

void braker_task(void *param) {
  int pressure_value = adc1_get_raw(ADC1_CHANNEL_0);
  int brake_pressure_return_value = 0;
  while (1) {
    pressure_value = adc1_get_raw(ADC1_CHANNEL_0);
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
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}



void app_main(void) {

//Joystick:
adc1_config_width(ADC_WIDTH_BIT_12);
adc1_config_channel_atten(ADC1_CHANNEL_0, ADC_ATTEN_DB_11);

  //Rotary encoder
  gpio_set_direction(ENCODER_CLK, GPIO_MODE_INPUT); 
  gpio_set_direction(ENCODER_DT, GPIO_MODE_INPUT);


    // dette er til at lave i2c linje og lave en lcd_task

    //lcd_init(LCD_ADDR, SDA_PIN, SCL_PIN, LCD_COLS, LCD_ROWS);
    //xTaskCreate(&lcd_task, "Demo Task", 2048, NULL, 5, NULL);

    xTaskCreate(&encoder_task, "Demo Task", 2048, NULL, 4, NULL);
    xTaskCreate(&braker_task, "Demo Task", 2048, NULL, 4, NULL);

    // dette er til at gemme SSID og Password
    nvs_init(); // Initialize NVS
    // dette er til at skabe forbindelse ti netværk
    wifi_init_sta(); // Initialize WiFi

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

