# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from os.path import exists
import time
from datetime import datetime
import board
import digitalio
from adafruit_bme280 import basic as adafruit_bme280
import csv

# Create sensor object, using the board's default I2C bus.
# i2c = board.I2C()  # uses board.SCL and board.SDA
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create sensor object, using the board's default SPI bus.
spi = board.SPI()
bme_cs = digitalio.DigitalInOut(board.D25)
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# field names
fields = ['Time', 'Temperature', 'Humidity', 'Pressure']

textfile = "/home/pi/EnviromentShare/current_data.txt"
while True:

  # name of csv file
  filename = "/home/pi/EnviromentShare/" + datetime.now().strftime("%y_%m_%d_") + "data.csv"

  if not exists(filename):
    # writing to csv file
    csvfile = open(filename, 'w')
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)
  else:
    # data rows of csv file
    data = [[datetime.now().strftime("%H:%M:%S"), round(bme280.temperature, 1), round(bme280.relative_humidity, 1), round(bme280.pressure, 1)]]

    csvfile =open(filename, 'a')
    csvwriter = csv.writer(csvfile)
    # writing the data rows
    csvwriter.writerows(data)

  csvfile.close()

  current_time = datetime.now()
  text = ""
  text += "Time: %d:%d\n" %(current_time.hour, current_time.minute)
  text += "Temp: %0.1f C\n" % bme280.temperature
  text += "Humi: %0.1f %%\n" % bme280.relative_humidity
  text += "Pres: %0.1f hPa" % bme280.pressure

  file = open(textfile, "w")
  file.write(text)
  file.close()

  time.sleep(30)


