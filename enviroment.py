# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import datetime
import board
import digitalio
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
# i2c = board.I2C()  # uses board.SCL and board.SDA
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create sensor object, using the board's default SPI bus.
spi = board.SPI()
bme_cs = digitalio.DigitalInOut(board.D25)
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

filename = "/home/pi/EnviromentShare/text.txt"
while True:
    current_time = datetime.datetime.now()
    text = ""
    text += "Time: %d:%d\n" %(current_time.hour, current_time.minute)
    text += "Temp: %0.1f C\n" % bme280.temperature
    text += "Humi: %0.1f %%\n" % bme280.relative_humidity
    text += "Pres: %0.1f hPa" % bme280.pressure


    file = open(filename, "w")
    file.write(text)
    file.close()

    time.sleep(2)

