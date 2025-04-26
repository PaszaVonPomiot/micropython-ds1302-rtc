# Micorpython DS1302 RTC Clock driver
A pure MicroPython driver for the DS1302 real-time clock (RTC) module.

# Dirver documentation
The DS1302 is a real-time clock (RTC) with a simple serial interface.

![](assets/images/ds1302.jpg)

## API Reference

- **`__init__(clk, dat, rst)`**  
  Initialize the DS1302 with clock, data, and reset pins.

- **`start()`**  
  Start the RTC.

- **`stop()`**  
  Stop/pause the RTC.

- **`date_time(date_time=None)`**  
  Get or set the full date and time.  
  - Without parameters: returns current `[year, month, day, weekday, hour, minute, second]`.
  - With a list parameter: sets the datetime.

- **`year(value=None)`**  
  Get or set the year.

- **`month(value=None)`**  
  Get or set the month.

- **`day(value=None)`**  
  Get or set the day.

- **`weekday(value=None)`**  
  Get or set the weekday.

- **`hour(value=None)`**  
  Get or set the hour.

- **`minute(value=None)`**  
  Get or set the minute.

- **`second(value=None)`**  
  Get or set the second.

- **`ram(register, data_byte=None)`**  
  Get or set RAM data (up to 31 bytes).

## Example Usage

```python
from ds1302 import DS1302
from machine import Pin

rtc = DS1302(clk=Pin(0), dat=Pin(1), rst=Pin(2))
rtc.date_time([2018, 3, 9, 4, 23, 0, 1])  # Set date and time

current_datetime = rtc.date_time()
current_time = f"{rtc.hour()}:{rtc.minute()}:{rtc.second()}"

print(current_datetime)  # [2018, 3, 9, 4, 23, 0, 1]
print(current_time)      # 23:0:1
```

## Acknowledgements
Thanks to previous authors and contributors:
- https://github.com/shaoziyang
- https://github.com/omarbenhamid