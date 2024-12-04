#include <stdio.h>
#include "driver/i2c_master.h" // New library that replaces "driver/i2c.h"
#include "driver/gpio.h"

#define I2C_MASTER_SDA_IO 6          // SDA Pin
#define I2C_MASTER_SCL_IO 7          // SCL Pin
#define I2C_MASTER_FREQ_HZ 100000    // Frequency
#define I2C_PORT_NUM_0 0            // I2C port number

i2c_master_bus_handle_t bus_handle;

void i2c_init(void)
{
    // Initialize the I2C master configuration using the new library
    i2c_master_bus_config_t i2c_mst_config = {
    .clk_source = I2C_CLK_SRC_DEFAULT,
    .i2c_port = I2C_PORT_NUM_0,
    .scl_io_num = I2C_MASTER_SCL_IO,
    .sda_io_num = I2C_MASTER_SDA_IO,
    .glitch_ignore_cnt = 7,
    .flags.enable_internal_pullup = true,
    };

    // Initialize I2C master with configured settings

    ESP_ERROR_CHECK(i2c_new_master_bus(&i2c_mst_config, &bus_handle));
}

void i2c_scan(void)
{
    // I2C scanning
    printf("Starting I2C scan...\n");
    for (uint8_t i = 1; i < 127; i++)
    {
        // Check if a device acknowledges at this address
        esp_err_t ret = i2c_master_probe(bus_handle, i, 2000);
        
        if (ret == ESP_OK)
        {
            printf("Found device at address: 0x%02X\n", i);
        }
        else
        {
            printf("No device found at address: 0x%02X\n", i);
        }
    }
    printf("I2C scan complete.\n");
}