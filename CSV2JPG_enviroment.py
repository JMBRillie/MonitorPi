
import time
from os.path import exists
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('dark_background')

imgname = "/home/pi/EnviromentShare/daily_data.jpg"

while True:

  filename = "/home/pi/EnviromentShare/" + datetime.now().strftime("%y_%m_%d_") + "data.csv"
  if not exists(filename):
    print( "Sleeping")

  else:
    with open(filename, 'r') as file:
      df = pd.read_csv(file)

      df['RT'] = df['Temperature'].rolling(10).mean()

      df['RH'] = df['Humidity'].rolling(10).mean()

      df['RP'] = df['Pressure'].rolling(10).mean()

      plt.subplot(3, 1, 1)
      a = plt.gca()
      xax = a.axes.get_xaxis()
      xax = xax.set_visible(False)
      plt.plot(df['Time'], df['RT'])

      plt.subplot(3, 1, 2)
      a = plt.gca()
      xax = a.axes.get_xaxis()
      xax = xax.set_visible(False)
      plt.plot(df['Time'], df['RH'])

      plt.subplot(3, 1, 3)
      a = plt.gca()
      xax = a.axes.get_xaxis()
      xax = xax.set_visible(False)
      plt.plot(df['Time'], df['RP'])

      plt.savefig(imgname)

      plt.clf()
      time.sleep(60)

