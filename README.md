# Micorpython DS1302 RTC Clock driver
A pure MicroPython driver for the DS1302 real-time clock (RTC) module.

# Dirver documentation
The DS1302 is a real-time clock (RTC) with a simple serial interface.

![](assets/images/ds1302.webp)

## API Reference

- **`__init__(clk, dat, rst)`**  
  Initialize the DS1302 with clock, data, and reset pins.

- **`start()`**  
  Start the RTC.

- **`stop()`**  
  Stop/pause the RTC.

- **`get_date_time()` / `set_date_time(date_time)`**  
  Get or set the full date and time.  
  - `get_date_time()`: returns current `[year, month, day, weekday, hour, minute, second]`.
  - `set_date_time(list)`: sets the datetime.

- **`get_year()` / `set_year(value)`**  
  Get or set the year.

- **`get_month()` / `set_month(value)`**  
  Get or set the month.

- **`get_day()` / `set_day(value)`**  
  Get or set the day.

- **`get_weekday()` / `set_weekday(value)`**  
  Get or set the weekday.

- **`get_hour()` / `set_hour(value)`**  
  Get or set the hour.

- **`get_minute()` / `set_minute(value)`**  
  Get or set the minute.

- **`get_second()` / `set_second(value)`**  
  Get or set the second.

- **`get_ram(register)` / `set_ram(register, value)`**  
  Get or set RAM data (up to 31 bytes).

## Example Usage

```python
from ds1302 import DS1302
from machine import Pin  # type: ignore[import]

# Initialize DS1302 RTC with the appropriate GPIO pins
rtc = DS1302(clk=Pin(0), dat=Pin(1), rst=Pin(2))

# Set the date and time: [year, month, day, weekday, hour, minute, second]
rtc.set_date_time([2084, 4, 26, 6, 14, 30, 0])  # Saturday, 14:30:00

# Or set the date and time using individual components
rtc.set_year(2025)

# Read the full date and time
print("Current date and time:", rtc.get_date_time())
# Output: [2025, 4, 26, 6, 14, 30, 0]

# Read individual components
year = rtc.get_year()
month = rtc.get_month()
day = rtc.get_day()
weekday = rtc.get_weekday()
hour = rtc.get_hour()
minute = rtc.get_minute()
second = rtc.get_second()

print(f"Year: {year}, Month: {month}, Day: {day}, Weekday: {weekday}")
print(f"Time: {hour:02}:{minute:02}:{second:02}")

# Save a 1-byte value (0-255) into one of RAM registers (0-30)
rtc.set_ram(register=30, value=255)

# Read the value back from RAM register
ram_reg_30 = rtc.get_ram(register=30)
print("Value from RAM:", ram_reg_30)
```

## Acknowledgements
Thanks to previous authors and contributors:
- https://github.com/shaoziyang
- https://github.com/omarbenhamid