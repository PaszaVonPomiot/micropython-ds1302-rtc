from machine import Pin  # type: ignore[import]

class _Reg:  # 8-bit register addresses
    SECOND = 0x80
    MINUTE = 0x82
    HOUR = 0x84
    DAY = 0x86
    MONTH = 0x88
    WEEKDAY = 0x8A
    YEAR = 0x8C
    WP = 0x8E  # Write protect register
    CTRL = 0x90  # Control register
    RAM = 0xC0  # RAM register (0xC0-0xFF)

class DS1302:
    def __init__(self, *, clk: Pin, dat: Pin, rst: Pin) -> None:
        self.pin_clk = clk
        self.pin_dat = dat
        self.pin_rst = rst
        self.pin_clk.init(Pin.OUT)
        self.pin_rst.init(Pin.OUT)

    def _dec2bcd(self, value: int) -> int:
        return (value // 10) * 16 + (value % 10)

    def _bcd2dec(self, value: int) -> int:
        return (value // 16) * 10 + (value % 16)

    def _write_byte(self, data_byte: int) -> None:
        self.pin_dat.init(Pin.OUT)
        for i in range(8):
            self.pin_dat.value((data_byte >> i) & 1)
            self.pin_clk.value(1)
            self.pin_clk.value(0)

    def _read_byte(self) -> int:
        data_byte = 0
        self.pin_dat.init(Pin.IN)
        for i in range(8):
            data_byte |= self.pin_dat.value() << i
            self.pin_clk.value(1)
            self.pin_clk.value(0)
        return data_byte

    def _get_register(self, register: int) -> int:
        self.pin_rst.value(1)
        self._write_byte(register)
        data_byte = self._read_byte()
        self.pin_rst.value(0)
        return data_byte

    def _set_register(self, register: int, value: int) -> None:
        self.pin_rst.value(1)
        self._write_byte(register)
        self._write_byte(value)
        self.pin_rst.value(0)

    def _wr(self, register: int, value: int) -> None:
        self._set_register(_Reg.WP, 0)
        self._set_register(register, value)
        self._set_register(_Reg.WP, 0x80)

    def start(self) -> None:
        sec = self._get_register(_Reg.SECOND + 1)
        self._wr(_Reg.SECOND, sec & 0x7F)

    def stop(self) -> None:
        sec = self._get_register(_Reg.SECOND + 1)
        self._wr(_Reg.SECOND, sec | 0x80)

    def second(self, value: int | None = None) -> int | None:
        if value is None:
            return self._bcd2dec(self._get_register(_Reg.SECOND + 1)) % 60
        self._wr(_Reg.SECOND, self._dec2bcd(value % 60))
        return None

    def minute(self, value: int | None = None) -> int | None:
        if value is None:
            return self._bcd2dec(self._get_register(_Reg.MINUTE + 1))
        self._wr(_Reg.MINUTE, self._dec2bcd(value % 60))
        return None

    def hour(self, value: int | None = None) -> int | None:
        if value is None:
            return self._bcd2dec(self._get_register(_Reg.HOUR + 1))
        self._wr(_Reg.HOUR, self._dec2bcd(value % 24))
        return None

    def weekday(self, value: int | None = None) -> int | None:
        if value is None:
            return self._bcd2dec(self._get_register(_Reg.WEEKDAY + 1))
        self._wr(_Reg.WEEKDAY, self._dec2bcd(value % 8))
        return None

    def day(self, value: int | None = None) -> int | None:
        if value is None:
            return self._bcd2dec(self._get_register(_Reg.DAY + 1))
        self._wr(_Reg.DAY, self._dec2bcd(value % 32))
        return None

    def month(self, value: int | None = None) -> int | None:
        if value is None:
            return self._bcd2dec(self._get_register(_Reg.MONTH + 1))
        self._wr(_Reg.MONTH, self._dec2bcd(value % 13))
        return None

    def year(self, value: int | None = None) -> int | None:
        if value is None:
            return self._bcd2dec(self._get_register(_Reg.YEAR + 1)) + 2000
        self._wr(_Reg.YEAR, self._dec2bcd(value % 100))
        return None

    def date_time(self, datetime: list[int|None] | None = None) -> list[int|None] | None:
        if datetime is None:
            return [
                self.year(),
                self.month(),
                self.day(),
                self.weekday(),
                self.hour(),
                self.minute(),
                self.second(),
            ]
        self.year(datetime[0])
        self.month(datetime[1])
        self.day(datetime[2])
        self.weekday(datetime[3])
        self.hour(datetime[4])
        self.minute(datetime[5])
        self.second(datetime[6])
        return None

    def ram(self, register: int, value: int | None = None) -> int | None:
        addr = _Reg.RAM + (register % 31) * 2
        if value is None:
            return self._get_register(addr + 1)
        self._wr(addr, value)
        return None
