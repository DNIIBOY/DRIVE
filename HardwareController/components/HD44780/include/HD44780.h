#ifndef HD44780_H
#define HD44780_H

// LCD module defines
#define LCD_LINEONE 0x00   // start of line 1
#define LCD_LINETWO 0x40   // start of line 2
#define LCD_LINETHREE 0x14 // start of line 3
#define LCD_LINEFOUR 0x54  // start of line 4

#define LCD_BACKLIGHT 0x08
#define LCD_ENABLE 0x04
#define LCD_COMMAND 0x00
#define LCD_WRITE 0x01

#define LCD_SET_DDRAM_ADDR 0x80
#define LCD_READ_BF 0x40

// LCD instructions register 
#define LCD_CLEAR 0x01             // replace all characters with ASCII 'space'
#define LCD_HOME 0x02              // return cursor to first position on first line
#define LCD_ENTRY_MODE 0x06        // shift cursor from left to right on read/write
#define LCD_DISPLAY_OFF 0x08       // turn display off
#define LCD_DISPLAY_ON 0x0C        // display on, cursor off, don't blink character
#define LCD_FUNCTION_RESET 0x30    // reset the LCD
#define LCD_FUNCTION_SET_4BIT 0x28 // 4-bit data, 2-line display, 5 x 8 font
#define LCD_SET_CURSOR 0x80        // set cursor position

// Initializes the LCD with specified I2C address and pins, as well as column and row count
void lcd_init(uint8_t addr, uint8_t dataPin, uint8_t clockPin, uint8_t cols, uint8_t rows);

// Sets the cursor position on the LCD (0-indexed)
void lcd_set_cursor(uint8_t col, uint8_t row);

// Sets cursor to the beginning of the first line
void lcd_cursor_first_line(void);

// Clears the LCD screen
void lcd_clear_screen(void);

// Writes a single character to the LCD
void lcd_write_char(char c);

// Writes a null-terminated string to the LCD
void lcd_write_str(char *str);

#endif // HD44780_H
