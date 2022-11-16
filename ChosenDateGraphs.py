
import subprocess
import time
from os.path import exists
from datetime import datetime
import pandas as pd
import numpy as np

shareDir = "/home/pi/EnviromentShare/"
if not exists(shareDir):
  os.mkdir(shareDir)

TGraph = shareDir + "T_graph.txt"
titleT = "\n\t\tTemperature [deg C]\t"
fixedDigitsT = "{:<5}"
dpT = 2

HGraph = shareDir + "H_graph.txt"
titleH = "\n\t\tHumidity [%]\t"
fixedDigitsH = "{:<5}"
dpH = 2

PGraph = shareDir + "P_graph.txt"
titleP = "\n\t\tPressure [kPa]\t"
fixedDigitsP = "{:<10}"
dpP = 4

numRows = 10

def createGraphFile(gName, avData, numCols, numRows, gTitle, timeNow, fixedDigits, dp):
  f = open(gName, "w")
  Max = avData.max()
  Min = avData.min()
  Range = Max - Min + 0.01
  newData = [0]*numCols
  i = int(avData.index[0])
  h = i
  while i < int(avData.index[-1])+1:
    if i == int(avData.index[h]):
      newData[i] =int( numRows*(float(avData[h]) - Min)/Range)
      h += 1
    else:
      newData[i] = -1
    i += 1
  f.write(gTitle + timeNow + "\n")
  for y in range(numRows,-1,-1):
    f.write(fixedDigits.format(str(round(Min + y*(Range/numRows),dp))) + "\t")
    for x in range(numCols):
      if int(newData[x]) == y:
        f.write(".#")
      else:
        f.write(". ")
    f.write(".\n") 
  f.write(fixedDigits.format("") + "\t")
  for hr in range(0,numCols,2):
    f.write(str(hr) + "  ")
    if hr < 10:
      f.write(" ")

  f.write("\n")
  f.close()

run = 1
while run:

  timeNow = input("Date of interest (yy_mm_dd): ")
#  timeNow = "22_09_22"
  filename = shareDir + timeNow + "_data.csv"
  if not exists(filename):
    print( "File for date not found")

  else:
    RtimeNow = timeNow[6:8] + timeNow[2:5] +timeNow[5] + timeNow[0:2]
    run = 0
    df = pd.read_csv(filename)
    df['Hour'] = df['Time']
    for i in range(df.shape[0]):
      try:
        df['Hour'] = df['Hour'].replace(df['Hour'].iloc[i],df['Hour'].iloc[i].split(":")[0])
      except:
        print ("Sad")
    numCols = int(df['Hour'].iloc[-1]) - int(df['Hour'].iloc[0]) + 1
    colDiv = int(df.shape[0]/numCols)

    avTemp = round(df.groupby('Hour')['Temperature'].mean(), dpT)
    createGraphFile(TGraph, avTemp, numCols, numRows, titleT, RtimeNow, fixedDigitsT, dpT)

    avHumi = round(df.groupby('Hour')['Humidity'].mean(), 2)
    createGraphFile(HGraph, avHumi, numCols, numRows, titleH, RtimeNow, fixedDigitsH, dpH)

    avPres = round(df.groupby('Hour')['Pressure'].mean(), 4)
    createGraphFile(PGraph, avPres, numCols, numRows, titleP, RtimeNow, fixedDigitsP, dpP)

    time.sleep(2)

    subprocess.run(["cat", TGraph])
    subprocess.run(["cat", HGraph])
    subprocess.run(["cat", PGraph])


