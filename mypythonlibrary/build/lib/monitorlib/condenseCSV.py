import os
from datetime import date
import pandas as pd

class PathError(Exception):
  pass

# Takes a month file in format: MONTH_YYYY.file
# Returns YYYY_MM to enable sorting month files
def IDMonth(monthFile):
  monthDict = {
    "Jan" : "01",
    "Feb" : "02",
    "Mar" : "03",
    "Apr" : "04",
    "May" : "05",
    "Jun" : "06",
    "Jul" : "07",
    "Aug" : "08",
    "Sep" : "09",
    "Oct" : "10",
    "Nov" : "11",
    "Dec" : "12"
  }
  month_num = ""
  ret = ''.join(monthFile.split('.')[0:-1]) #Remove file extention
  ret = ''.join(ret.split('_')[-1])  #Remove the month name (keep only the year)
  ret = f"{ret}_{monthDict[monthFile[0:3]]}"
  return ret  # Returns YYYY_MM to enable sorting month files

class Condense:
  def __init__(self, csv_dir) -> None:
    self.csvDir = csv_dir
    self.daysDir = self.csvDir + "days/"
    self.monthsDir = self.csvDir + "months/"
    self.yearsDir = self.csvDir + "years/"
    self.checkDirs()

  def checkDirs(self):
    if not os.path.exists(self.csvDir):
      raise PathError(f"{self.csvDir} not found")
    if not os.path.exists(self.daysDir):
      raise PathError(f"{self.daysDir} not found")
    if not os.path.exists(self.monthsDir):
      os.mkdir(self.monthsDir)
    if not os.path.exists(self.yearsDir):
      os.mkdir(self.yearsDir)

  def year(self, year): # YYYY
    print (f"Processing:\t {year}")
    months_list = [ f for f in os.listdir(self.monthsDir) if (f.endswith(".csv") and year in f )]
    months_list.sort(key=IDMonth)
    newYear = 1
    for csvName in months_list:
      year_file = f"{self.yearsDir}{year}.csv"
      # Import the csv data into pandas dataframe
      df = pd.read_csv(self.monthsDir + csvName)
      # Average the data for each day in the month
      day_average = df.groupby(['Year','Month','Day'])[['Temperature','Humidity','Pressure']].mean().round(2)
      # Save the data
      if newYear:
        day_average.to_csv(year_file, mode='w', header=True)
        newYear = 0
      else:
        day_average.to_csv(year_file, mode='a', header=False)

  def month(self, month):  # MONTH_YYYY
    print (f"Processing:\t {month}")
    # List all csv files in daysDir
    file_list = [ f for f in os.listdir(self.daysDir) if f.endswith(".csv")]
    # Select the days in the chosen month
    days_list = []
    for csvName in file_list:
      dateYY_MM_DD = csvName[0:8]
      YYYY =  "20" + dateYY_MM_DD[0:2]
      MM =  dateYY_MM_DD[3:5]
      DD =  dateYY_MM_DD[6:8]
      monthName = date(day=int(DD), month=int(MM), year=int(YYYY)).strftime("%B_%Y")
      if monthName == month:
        days_list.append(csvName)
    days_list.sort()

    newMonth = 1
    for csvName in days_list:
      month_file = f"{self.monthsDir}{month}.csv"
      # Import the csv data into pandas dataframe
      df = pd.read_csv(self.daysDir + csvName)
      # Split time into hours, minutes, and seconds
      df[['Hour','Minute','Second']] = df['Time'].str.split(':', expand=True)
      # Create year, month, and day columns
      dateYY_MM_DD = csvName[0:8]
      df['Year'] = "20" + dateYY_MM_DD[0:2]
      df['Month'] = dateYY_MM_DD[3:5]
      df['Day'] = dateYY_MM_DD[6:8]
      # Average the data for each hour in the day
      hourly_average = df.groupby(['Year','Month','Day','Hour'])[['Temperature','Humidity','Pressure']].mean().round(2)
      # Save the data
      if newMonth:
        hourly_average.to_csv(month_file, mode='w', header=True)
        newMonth = 0
      else:
        hourly_average.to_csv(month_file, mode='a', header=False)

if __name__ == "__main__":
  condense = Condense("/home/pi/bedroom_data/CSV_files/") 
  condense.month("May_2023")
  condense.year("2023")
