#ifndef HD44780_H
#define HD44780_H
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
