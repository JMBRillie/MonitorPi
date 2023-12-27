
from calendar import month
import os
import copy

class PathError(Exception):
  pass

class Generator:
  def __init__(self, shareDir) -> None:
    self.shareDir = shareDir
    self.plotsDir = self.shareDir + "Plots/"
    self.folder = ""
    self.htmlDir = self.shareDir + "html/"
    #self.mobileDir = self.shareDir + "m/"
    #self.m_htmlDir = self.mobileDir + "html/"
    self.csvDir = self.shareDir + "CSV_files/"
    self.checkDirs()

  def checkDirs(self):
    if not os.path.exists(self.plotsDir):
      raise PathError(f"{self.plotsDir} not found")
    if not os.path.exists(self.csvDir):
      raise PathError(f"{self.csvDir} not found")
    if not os.path.exists(self.htmlDir):
      os.mkdir(self.htmlDir)
  #  if not os.path.exists(self.mobileDir):
   #   os.mkdir(self.mobileDir)
  #  if not os.path.exists(self.m_htmlDir):
   #   os.mkdir(self.m_htmlDir)

  def checkFolder(self):
    if not os.path.exists(self.plotsDir + self.folder):
      raise PathError(f"{self.plotsDir}{self.folder} not found")
    if not os.path.exists(self.csvDir + self.folder):
      raise PathError(f"{self.csvDir}{self.folder} not found")
    if not os.path.exists(self.htmlDir + self.folder):
      os.mkdir(self.htmlDir + self.folder)
#    if not os.path.exists(self.m_htmlDir + self.folder):
 #     os.mkdir(self.m_htmlDir + self.folder)

  def loadPlots(self):
    self.plots_list = os.listdir(self.plotsDir + self.folder)
    if self.folder == "months/":
      self.plots_list.sort(key=IDMonth)
    else:
      self.plots_list.sort()
    self.num_plots = len(self.plots_list)

  def loadPages(self):
    self.pages_list = os.listdir(self.htmlDir + self.folder)
    if self.folder == "months/":
      self.pages_list.sort(key=IDMonth)
    else:
      self.pages_list.sort()
    self.num_pages = len(self.pages_list)

  def makePage(self, plotNames):
    baseName = plotNames[1].split('.')[0]
    pageName = baseName + ".html"
    csvName = baseName + ".csv"

    page = DataPage(self.htmlDir + self.folder, pageName)
    page.setNames(self.plotsDir + self.folder, plotNames)
    page.setMaxMin(self.csvDir + self.folder, csvName)
    page.writePage()

#    m_plotNames = [P.split('.')[0] + "_m.png" for P in plotNames]
#    m_page = DataPage(self.m_htmlDir + self.folder, pageName)
#    m_page.setNames(self.plotsDir + self.folder, m_plotNames)
#    m_page.setMaxMin(self.csvDir + self.folder, csvName)
#    m_page.writePage()

    return (1)

  def processFolder(self):
    self.checkFolder()
    self.loadPlots()
    plotNames = ["","",""]
    for plot_name in self.plots_list:
      plotNames[0] =  self.plots_list[(self.plots_list.index(plot_name) - 1) % self.num_plots]
      plotNames[1] =  plot_name
      plotNames[2] =  self.plots_list[(self.plots_list.index(plot_name) + 1) % self.num_plots]
      print (f"Processing:\t{plot_name}")
      self.makePage(plotNames)
      print (f"\t\t\t{plot_name} complete")
    self.loadPages()
    self.makeChoosePage()

  def makeChoosePage(self):
    choose_page = ChoosePage(self.shareDir, f'choose_{self.folder.removesuffix("s/")}.html')
    choose_page.headerTitle = f'Choose a {self.folder.removesuffix("s/")} to view'
    choose_page.style_sheets.append("/bedroom_data/choose_style.css")
    choose_page.setContentLists(self. pages_list)
    choose_page.setContent()
    choose_page.writePage()

class Page:
  def __init__(self, pageDir, pageName) -> None:
    self.file = open(pageDir + pageName, 'w')
    self.pageTitle = os.path.splitext(os.path.basename(pageName))[0]
    self.style_sheets = ["/bedroom_data/generic_style.css"]
    self.headerTitle = "Bedroom Data"
    self.footer_message = "Speak to Jake to find out more"

  def writeHead(self):
    self.file.write('<head>\n')
    self.file.write(f'<title>{self.pageTitle}</title>\n')
    for style_sheet in self.style_sheets:
      self.file.write(f'<link rel="stylesheet" type="text/css" href="{style_sheet}"/>\n')
    self.file.write('<meta charset="utf-8">')
    self.file.write('</head>\n')

  def writeHeader(self):
    self.file.write(f'<div id="header"> <h1>{self.headerTitle}</h1> </div>\n')

  def writeCommonNavButtons(self):
    self.file.write('<div class="nav_A" id="home"> <a href="/">Home</a> </div>\n')
    self.file.write('<div class="nav_B" id="choose-day"> <a href="/bedroom_data/choose_day.html">Choose Day</a> </div>\n')
    self.file.write('<div class="nav_A" id="choose-month"> <a href="/bedroom_data/choose_month.html">Choose Month</a> </div>\n')
    self.file.write('<div class="nav_B" id="choose-year"> <a href="/bedroom_data/choose_year.html">Choose Year</a> </div>\n')

  def writeSpecialNavButtons(self):
    pass

  def writeNav(self):
    self.file.write('<div id="nav">\n')
    self.writeCommonNavButtons()
    self.writeSpecialNavButtons()
    self.file.write('</div>\n')

  def writeContent(self):
    self.file.write('<div id="content"> </div>\n')

  def writeShortcuts(self):
    self.file.write('<div class="shortcuts"> </div>\n')

  def writeFooter(self):
    self.file.write(f'<div id="footer">\n{self.footer_message}\n</div>\n')

  def writeContainer(self):
    self.file.write('<div id="container">\n')
    self.writeHeader()
    self.writeNav()
    self.writeContent()
    self.writeShortcuts()
    self.writeFooter()
    self.file.write('</div>\n')

  def writeBody(self):
    self.file.write('<body>\n')
    self.writeContainer()
    self.file.write('</body>\n')

  def writePage(self):
    self.file.write('<!DOCTYPE html>\n<html>\n')
    self.writeHead()
    self.writeBody()
    self.file.write('</html>\n')
    self.file.close()

class DataPage(Page):
  def __init__(self, pageDir, pageName) -> None:
    super().__init__(pageDir, pageName)
    self.plotsDir = ""
    self.monthPage = ""
    self.yearPage = ""
    self.max_t = 0.0
    self.max_p = 0.0
    self.max_h = 0.0
    self.min_t = 0.0
    self.min_p = 0.0
    self.min_h = 0.0

  def setNames(self, plotsDir,  plotNames):
    self.plotsDir = plotsDir
    self.plotsRefDir = f'/bedroom_data/Plots/{"/".join(plotsDir.split("/")[-2:])}'
    self.plotNames = plotNames
    self.pageNames = ["","",""]
    self.baseNames = ["","",""]
    for i in range(3):
      if not os.path.exists(self.plotsDir + self.plotNames[i]):
        raise PathError(f"{self.plotNames[i]} not found in: {self.plotsDir}")
      self.baseNames[i] = os.path.splitext(os.path.basename(self.plotNames[i]))[0]
      self.pageNames[i] = self.baseNames[i] + ".html"
    if "data" in self.plotNames[1]: # Day page
      self.monthPage = f"{inv_monthDict[self.pageNames[1][3:5]]}_20{self.pageNames[1][0:2]}.html"
      self.yearPage = f"20{self.pageNames[1][0:2]}.html"
    elif "_" in self.plotNames[1]:  # Month page
      self.yearPage = f"20{self.baseNames[1][-2:]}.html"

  def setMaxMin(self, csvDir, csvName):
    with open(csvDir + csvName, 'r') as c:
      header = c.readline()
      data = []
      for line in c.readlines():
        data.append([float(cell) for cell in line.split(',')[-3:]])
      self.max_t, self.min_t, self.max_h, self.min_h, self.max_p, self.min_p = data[0][-3], data[0][-3], data[0][-2], data[0][-2], data[0][-1], data[0][-1]
      for line in data:
        if line[-3] > self.max_t:
          self.max_t = line[-3]
        if line[-3] < self.min_t:
          self.min_t = line[-3]
        if line[-2] > self.max_h:
          self.max_h = line[-2]
        if line[-2] < self.min_h:
          self.min_h = line[-2]
        if line[-1] > self.max_p:
          self.max_p = line[-1]
        if line[-1] < self.min_p:
          self.min_p = line[-1]

  def writeSpecialNavButtons(self):
    self.file.write(f'<div> </div>\n')
    self.file.write(f'<div class="max_min" id="temp"> Temperature <p>Max: {self.max_t}°C</p> <p>Min: {self.min_t}°C</p> </div>')
    self.file.write(f'<div class="max_min" id="humi"> Humidity <p>Max: {self.max_h}%</p> <p>Min: {self.min_h}%</p> </div>')
    self.file.write(f'<div class="max_min" id="pres"> Pressure <p>Max: {self.max_p}MPa</p> <p>Min: {self.min_p}MPa</p> </div>')

  def writeContent(self):
    self.file.write('<div id="content">\n')
    self.file.write(f'<img src="{self.plotsRefDir}{self.plotNames[1]}" alt="{self.plotNames[1]}">\n')
    self.file.write('</div>\n')

  def writeShortcuts(self):
    self.file.write('<div class="shortcuts">\n')
    self.file.write(f'<div class="shortcut_A" id="previous"> <a href="{self.pageNames[0]}">Previous</a> </div>\n')
    if self.monthPage != "":  # day file
      self.file.write(f'<div class="shortcut_B" id="view-month"> <a href="../months/{self.monthPage}">View Month</a> </div>\n')
      self.file.write(f'<div class="shortcut_B" id="view-year"> <a href="../years/{self.yearPage}">View Year</a> </div>\n')
    elif self.yearPage != "": # month file
      self.file.write(f'<div class="shortcut_C"> </div>\n')
      self.file.write(f'<div class="shortcut_B" id="view-year"> <a href="../years/{self.yearPage}">View Year</a> </div>\n')
      self.file.write(f'<div class="shortcut_C"> </div>\n')
    else:  # year file
      self.file.write(f'<div class="shortcut_D"> </div>\n')
    self.file.write(f'<div class="shortcut_A" id="next"> <a href="{self.pageNames[2]}">Next</a> </div>\n')
    self.file.write('</div>\n')

class ChoosePage(Page):
  def __init__(self, pageDir, pageName) -> None:
    super().__init__(pageDir, pageName)
    self.years = []

  def setContentLists(self, pages_list):
    self.years_list_YYYY = []
    self.months_list_MM = [[]]
    self.days_list_DD = [[[]]]

    if "data" in pages_list[0]:
      self.folder = "days/"
    elif "_" in pages_list[0]:
      self.folder = "months/"
    else:
      self.folder = "years/"

    # Create a list of the years
    for page_name in pages_list:
      if self.folder == "days/":
        YYYY = "20" + page_name[0:2]
      else:  # for both months and years YY is the two characters before ".html"
        YYYY = "20" + page_name[-7:-5]
      if YYYY not in self.years_list_YYYY:
        self.years_list_YYYY.append(YYYY)
    ## years_list_YYYY is now a list of all the years we need to include

    # Resize months_list to fit each year
    for YYYY in self.years_list_YYYY:
      if self.years_list_YYYY.index(YYYY):
        self.months_list_MM.append([])

    self.month_names = copy.deepcopy(self.months_list_MM)  # month_names will be MONTH

    if not self.folder == "years/":
      # Create a list of months in each year
      for page_name in pages_list:
        if self.folder == "days/":
          YYYY = "20" + page_name[0:2]
          MM = page_name[3:5]
        else:  # If not day, then month
          YYYY = page_name[-9:-5]
          MM = monthDict[page_name[:-10]]
        yr_idx = self.years_list_YYYY.index(YYYY)
        if MM not in self.months_list_MM[yr_idx]:
          self.months_list_MM[yr_idx].append(MM)
          self.month_names[yr_idx].append(inv_monthDict[MM])

      if self.folder == "days/":
        # Resize days_list to fit each year and month
        for YYYY in self.years_list_YYYY:
          yr_idx = self.years_list_YYYY.index(YYYY)
          if yr_idx:
            self.days_list_DD.append([[]])
          for MM in self.months_list_MM[yr_idx]:
            if self.months_list_MM[yr_idx].index(MM):
              self.days_list_DD[yr_idx].append([])

        self.day_page_names = copy.deepcopy(self.days_list_DD)  # day_page_names will be YY_MM_DD_data.html

        # Create a list of days in each month in each year
        for page_name in pages_list:
          YYYY = "20" + page_name[0:2]
          MM = page_name[3:5]
          DD = page_name[6:8]
          yr_idx = self.years_list_YYYY.index(YYYY)
          mn_idx = self.months_list_MM[yr_idx].index(MM)
          if DD not in self.days_list_DD[yr_idx][mn_idx]:
            self.days_list_DD[yr_idx][mn_idx].append(DD)
            self.day_page_names[yr_idx][mn_idx].append(page_name)

  def setContent(self):
    for YYYY in self.years_list_YYYY:
      yr_idx = self.years_list_YYYY.index(YYYY)
      year = pageLinkDiv(YYYY, YYYY + ".html")
      if self.folder != "years/":
        for MM in self.months_list_MM[yr_idx]:
          mn_idx = self.months_list_MM[yr_idx].index(MM)
          mn_name = self.month_names[yr_idx][mn_idx]
          mn_pageName = f"{mn_name}_{YYYY}.html"
          month = pageLinkDiv(mn_name, mn_pageName)
          if self.folder == "days/":
            for DD in self.days_list_DD[yr_idx][mn_idx]:
              dy_idx = self.days_list_DD[yr_idx][mn_idx].index(DD)
              day = pageLinkDiv(DD, self.day_page_names[yr_idx][mn_idx][dy_idx])
              month.subDivs.append(day)
          if not mn_idx % 4:
            ML = pageLinkDiv("Month Line", "Month Line")
            year.subDivs.append(ML)
          ML.subDivs.append(month)
      self.years.append(year)

  def writeYear(self, year):
    self.file.write('<div class="year">\n')
    self.file.write(f'<h2> <a href="html/years/{year.pageName}">{year.name}</a> </h2>\n')
    for monthLine in year.subDivs:
      self.file.write('<div class="month_line">\n')
      for month in monthLine.subDivs:
        self.file.write('<div class="month">')
        self.file.write(f'<h3> <a href="html/months/{month.pageName}">{month.name}</a> </h3>\n')
        for day in month.subDivs:
          self.file.write('<div class="day">')
          self.file.write(f'<a href="html/days/{day.pageName}">{day.name}</a>')
          self.file.write('</div>\n')
        self.file.write('</div>\n')
      self.file.write('</div>\n')
    self.file.write('</div>\n')

  def writeContent(self):
    self.file.write('<div id="content">\n')
    for year in self.years:
      self.writeYear(year)
    self.file.write('</div>\n')

class HomePage(DataPage):
  def __init__(self, pageDir, pageName) -> None:
    super().__init__(pageDir, pageName)
    self.style_sheets.append("home_style.css")
    self.plotsRefDir = "/bedroom_data/Plots/days/"
    self.latestPlot = ""
    self.yesterdayPage = ""
    self.monthPage = ""
    self.yearPage = ""

  def writeContent(self):
    self.file.write('<div id="content">\n')
    self.file.write(f'<img src="{self.plotsRefDir}{self.latestPlot}" alt="latest_plot.png">\n')
    self.file.write('</div>\n')

  def writeShortcuts(self):
    self.file.write('<div class="shortcuts">\n')
    self.file.write(f'<div class="shortcut_A" id="yesterday"> <a href="{self.yesterdayPage}">Yesterday</a> </div>\n')
    self.file.write(f'<div class="shortcut_B" id="c_month"> <a href="{self.monthPage}">Current Month</a> </div>\n')
    self.file.write(f'<div class="shortcut_A" id="c_year"> <a href="{self.yearPage}">Current Year</a> </div>\n')
    self.file.write('</div>\n')

class pageLinkDiv:
  def __init__(self, name, pageName) -> None:
    self.name = name
    self.pageName = pageName
    self.subDivs = []

monthDict = {
  "January"   : "01",
  "February"  : "02",
  "March"     : "03",
  "April"     : "04",
  "May"       : "05",
  "June"      : "06",
  "July"      : "07",
  "August"    : "08",
  "September" : "09",
  "October"   : "10",
  "November"  : "11",
  "December"  : "12"
  }

inv_monthDict = {v:k for k, v in monthDict.items()}

# Takes a month file in format: MONTH_YYYY.file
# Returns YYYY_MM to enable sorting month files
def IDMonth(monthFile):
  month_yyyy = monthFile.split('.')[0] # Remove file extention
  month, yyyy = month_yyyy.split('_')
  return (f"{yyyy}_{monthDict[month]}")  # Returns YYYY_MM to enable sorting month files

if __name__ == "__main__":
  shareDir = "/shares/Enviromental/Bedroom/"
  gen = Generator(shareDir)
  folders = ["days/", "months/", "years/"]
  for folder in folders:
    gen.folder = folder
    gen.processFolder()

