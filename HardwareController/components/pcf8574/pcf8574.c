#include "driver/i2c_master.h"
#include <esp_log.h>
#include <freertos/FreeRTOS.h>
#include <stdio.h>
/*
i2c_master_dev_handle_t dev_handle;

i2c_master_dev_handle_t pcf8574_init(i2c_master_bus_handle_t bus_handle, i2c_device_config_t dev_cfg,) {


    esp_err_t ret = i2c_master_bus_add_device(bus_handle, &dev_cfg, &dev_handle);
    if (ret != ESP_OK) {
        ESP_LOGE("PCF8574", "Failed to add device to I2C bus: %s", esp_err_to_name(ret));
    }

    return dev_handle;
}

esp_err_t pcf8574_write_port(i2c_master_dev_handle_t dev_handle, uint8_t data) {
    esp_err_t ret = i2c_master_write_byte(dev_handle, data, I2C_MASTER_WRITE);
    if (ret != ESP_OK) {
        ESP_LOGE("PCF8574", "Failed to write to device: %s", esp_err_to_name(ret));
        return ret;
    }

    return ESP_OK;
}

esp_err_t pcf8574_read_port(i2c_master_dev_handle_t dev_handle, uint8_t *data) {
    esp_err_t ret = i2c_master_read_byte(dev_handle, data, I2C_MASTER_READ);
    if (ret != ESP_OK) {
        ESP_LOGE("PCF8574", "Failed to read from device: %s", esp_err_to_name(ret));
        return ret;
    }

    return ESP_OK;
}
*/