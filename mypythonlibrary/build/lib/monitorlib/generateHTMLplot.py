
import os
import copy

shareDir = "/shares/Enviromental/Bedroom/"
plotsDir = shareDir + "Plots/"
days_plotsDir = plotsDir + "days/"
months_plotsDir = plotsDir + "months/"
years_plotsDir = plotsDir + "years/"

htmlDir = shareDir + "html/"
days_htmlDir = htmlDir + "days/"
months_htmlDir = htmlDir + "months/"
years_htmlDir = htmlDir + "years/"


for dir in [plotsDir, days_plotsDir, months_plotsDir, years_plotsDir]:
  if not os.path.exists(dir):
    print (dir + "  not found")
    exit()
for dir in [htmlDir, days_htmlDir, months_htmlDir, years_htmlDir]:
  if not os.path.exists(dir):
    os.mkdir(dir)

def monthNameFromNum(MM):
  if MM == "01":
    return ("January")
  if MM == "02":
    return ("February")
  if MM == "03":
    return ("March")
  if MM == "04":
    return ("April")
  if MM == "05":
    return ("May")
  if MM == "06":
    return ("June")
  if MM == "07":
    return ("July")
  if MM == "08":
    return ("August")
  if MM == "09":
    return ("September")
  if MM == "10":
    return ("October")
  if MM == "11":
    return ("November")
  if MM == "12":
    return ("December")
  return("Month name error")

def monthNumFromName(month):
  if month == "January":
    return ("01")
  if month == "February":
    return ("02")
  if month == "March":
    return ("03")
  if month == "April":
    return ("04")
  if month == "May":
    return ("05")
  if month == "June":
    return ("06")
  if month == "July":
    return ("07")
  if month == "August":
    return ("08")
  if month == "September":
    return ("09")
  if month == "October":
    return ("10")
  if month == "November":
    return ("11")
  if month == "December":
    return ("12")
  return("Month name error")


# Returns YYYY_MM to enable sorting month files
def IDMonth(monthFile):  # Month file in format: MONTH_YYYY.file
  month_num = ""
  if "Jan" in monthFile:
    month_num = "_01"
  if "Feb" in monthFile:
    month_num = "_02"
  if "Mar" in monthFile:
    month_num = "_03"
  if "Apr" in monthFile:
    month_num = "_04"
  if "May" in monthFile:
    month_num = "_05"
  if "Jun" in monthFile:
    month_num = "_06"
  if "Jul" in monthFile:
    month_num = "_07"
  if "Aug" in monthFile:
    month_num = "_08"
  if "Sep" in monthFile:
    month_num = "_09"
  if "Oct" in monthFile:
    month_num = "_10"
  if "Nov" in monthFile:
    month_num = "_11"
  if "Dec" in monthFile:
    month_num = "_12"
  if month_num == "":
    return "Error in month name"
  ret = ''.join(monthFile.split('.')[0:-1]) #Remove file extention
  ret = ''.join(ret.split('_')[-1:])  #Remove the month name (keep only the year)
  ret = ret + month_num
  return ret  # Returns YYYY_MM to enable sorting month files

def makePage(plotNames):
  day = 0
  month = 0
  year = 0
  folder = ""
  if "data" in plotNames[1]:
    day = 1;
    folder = "days/"
  elif "_" in plotNames[1]:
    month = 1
    folder = "months/"
  elif "20" == plotNames[1][0:2]:
    years = 1
    folder = "years/"

  pageNames = ["","",""]
  baseNames = ["","",""]
  for i in range(3):
    if not os.path.exists(plotsDir + folder + plotNames[i]):
      print (plotNames[i] + " not found in: " + plotsDir + folder)
      return (0)
    baseNames[i] = os.path.splitext(os.path.basename(plotNames[i]))[0]
    pageNames[i] = baseNames[i] + ".html"

  with open(htmlDir + folder + pageNames[1], 'w') as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<head>\n")
    f.write("<title>" + baseNames[1] + "</title>\n")
    f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"/bedroom_data/generic_style.css\"/>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<div id=\"container\">\n")
    f.write("<div id=\"header\">\n")
    f.write("<h1>Bedroom Data</h1>\n")
    f.write("</div>\n") #close header
    f.write("<div id=\"content\">\n")
    f.write("<div id=\"nav\">\n")
    f.write("<div class=\"nav_A\" id=\"home\"> <a href=\"/\">Home</a> </div>\n")
    f.write("<div class=\"nav_B\" id=\"choose-day\"> <a href=\"/bedroom_data/choose_day.html\">Choose Day</a> </div>\n")
    f.write("<div class=\"nav_A\" id=\"choose-day\"> <a href=\"/bedroom_data/choose_month.html\">Choose Month</a> </div>\n")
    f.write("<div class=\"nav_B\" id=\"choose-year\"> <a href=\"/bedroom_data/choose_year.html\">Choose Year</a> </div>\n")
    if day:
      monthPage = monthNameFromNum(pageNames[1][3:5]) + "_20" + pageNames[1][0:2] + ".html"
      f.write("<div class=\"nav_SC_A\" id=\"view-month\"> <a href=\"../months/" + monthPage + "\">View Month</a> </div>\n")
      yearPage = "20" + pageNames[1][0:2] + ".html"
      f.write("<div class=\"nav_SC_B\" id=\"view-year\"> <a href=\"../years/" + yearPage + "\">View Year</a> </div>\n")
    elif month:
      yearPage = "20" + baseNames[1][-2:] + ".html"
      f.write("<div class=\"nav_SC_A\" id=\"view-year\"> <a href=\"../years/" + yearPage + "\">View Year</a> </div>\n")
    f.write("</div>\n") # close nav
    f.write("<div id=\"main\">\n")
    f.write("<img src=\"/bedroom_data/Plots/" + folder + plotNames[1] + "\" alt=\"" + plotNames[1] + "\">\n")
    f.write("</div>\n") # close main
    f.write("<div id=\"shortcuts\">\n")
    f.write("<div class=\"shortcut_A\" id=\"previous\"> <a href=\"" + pageNames[0] + "\">Previous</a> </div>\n")
    f.write("<div class=\"shortcut_B\" id=\"next\"> <a href=\"" + pageNames[2] + "\">Next</a> </div>\n")
    f.write("</div>\n") # close shortcuts
    f.write("</div>\n") # close content
    f.write("</body>\n")
    f.write("</html>\n")

  return (1)


def processFolder(folder):
  plots_list = os.listdir(plotsDir + folder)
  if folder == "months/":
    plots_list.sort(key=IDMonth)
  else:
    plots_list.sort()

  plotNames = ["","",""]
  for plot_name in plots_list:
    plotNames[0] =  plots_list[(plots_list.index(plot_name) - 1) % len(plots_list)]
    plotNames[1] =  plot_name
    plotNames[2] =  plots_list[(plots_list.index(plot_name) + 1) % len(plots_list)]
    print ("Processing:\t" + plot_name)
    if not makePage(plotNames):
      print ("\t\t*** " + plot_name + " *** Failed")
    else:
      print ("\t\t" + plot_name + " complete")

def makeChoosePage(type):
  if type == "day":
    choosePageName = shareDir + "choose_day.html"
    activeDir = days_htmlDir
  elif type == "month":
    choosePageName = shareDir + "choose_month.html"
    activeDir = months_htmlDir
  elif type == "year":
    choosePageName = shareDir + "choose_year.html"
    activeDir = years_htmlDir
  else:
    print ("Wrong type chosen for generation of a choose page")
    return(0)

  years_list_YY = []
  months_list_MM = [[]]
  days_list_DD = [[[]]]

  pages_list = os.listdir(activeDir)
  if type == "month":
    pages_list.sort(key=IDMonth)
  else:
    pages_list.sort()
  ## pages_list is now a sorted list of all the html files we want to include in our choose page

  # Create a list of the years
  for page_name in pages_list:
    if type == "day":
      YY = page_name[0:2]
    else:  # for both months and years YY is the two characters before ".html"
      YY = page_name[-7:-5]
    if YY not in years_list_YY:
      years_list_YY.append(YY)
  ## years_list_YY is now a list of all the years we need to include

  # Resize months_list to fit each year
  for YY in years_list_YY:
    if years_list_YY.index(YY):
      months_list_MM.append([])

  month_names = copy.deepcopy(months_list_MM)  # month_names will be MONTH

  if not type == "year":
    # Create a list of months in each year
    for page_name in pages_list:
      if type == "day":
        YY = page_name[0:2]
        MM = page_name[3:5]
      else:  # If not day, then month
        YY = page_name[-7:-5]
        MM = monthNumFromName(page_name[:-10])
      yr_idx = years_list_YY.index(YY)
      if MM not in months_list_MM[yr_idx]:
        months_list_MM[yr_idx].append(MM)
        month_names[yr_idx].append(monthNameFromNum(MM))

    if type == "day":
      # Resize days_list to fit each year and month
      for YY in years_list_YY:
        yr_idx = years_list_YY.index(YY)
        if yr_idx:
          days_list_DD.append([[]])
        for MM in months_list_MM[yr_idx]:
          if months_list_MM[yr_idx].index(MM):
            days_list_DD[yr_idx].append([])

      day_page_names = copy.deepcopy(days_list_DD)  # day_page_names will be YY_MM_DD_data.html

      # Create a list of days in each month in each year
      for page_name in pages_list:
        YY = page_name[0:2]
        MM = page_name[3:5]
        DD = page_name[6:8]
        yr_idx = years_list_YY.index(YY)
        mn_idx = months_list_MM[yr_idx].index(MM)
        if DD not in days_list_DD[yr_idx][mn_idx]:
          days_list_DD[yr_idx][mn_idx].append(DD)
          day_page_names[yr_idx][mn_idx].append(page_name)

  with open(choosePageName, 'w') as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<head>\n")
    f.write("<title>Choose " + type.title() + "</title>\n")
    f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"choose_style.css\"/>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<div id=\"container\">\n")
    f.write("<div id=\"header\">\n")
    f.write("<h1>Choose a " + type + " to view</h1>\n")
    f.write("</div>\n")
    f.write("<div id=\"content\">\n")
    f.write("<div id=\"nav\">\n")
    f.write("<div class=\"nav_A\" id=\"home\"> <a href=\"/\">Home</a> </div>\n")
    f.write("<div class=\"nav_B\" id=\"choose-day\"> <a href=\"choose_day.html\">Choose Day</a> </div>\n")
    f.write("<div class=\"nav_A\" id=\"choose-month\"> <a href=\"choose_month.html\">Choose Month</a> </div>\n")
    f.write("<div class=\"nav_B\" id=\"choose-year\"> <a href=\"choose_year.html\">Choose Year</a> </div>\n")
    f.write("</div>\n") # Close nav
    f.write("<div id=\"main\">\n")
    for YY in years_list_YY:
      yr_idx = years_list_YY.index(YY)
      f.write("<div class=\"year\">\n")
      year_page_name = "20" + YY + ".html"
      f.write("<h2> <a href=\"html/years/" + year_page_name +"\">20" + YY + "</a> </h2>\n")
      if not type == "year":
        for MM in months_list_MM[yr_idx]:
          mn_idx = months_list_MM[yr_idx].index(MM)
          if not mn_idx % 4:
            f.write("<div class=\"month_line\">\n")
          month_page_name = month_names[yr_idx][mn_idx] + "_20" + YY + ".html"
          f.write("<div class=\"month\"> <h3> <a href=\"html/months/" + month_page_name +  "\">" + month_names[yr_idx][mn_idx] + "</a> </h3>\n")
          if type == "day":
            for DD in days_list_DD[yr_idx][mn_idx]:
              dy_idx = days_list_DD[yr_idx][mn_idx].index(DD)
              f.write("<div class=\"day\"> <a href=\"html/days/" + day_page_names[yr_idx][mn_idx][dy_idx] + "\">" + DD + "</a> </div>\n")
          f.write("</div>\n") # close month
          if (mn_idx % 4) == 3:
            f.write("</div>\n") # close month line after every 4th month
        if not (mn_idx % 4) == 3:
          f.write("</div>\n") # close month line if not closed by reaching 4th month in last line

      f.write("</div>\n") # close year

    f.write("</div>\n") # close main
    f.write("</div>\n") # close content

    f.write("<div id=\"footer\">\n")
    f.write("Speak to Jake for more information\n")
    f.write("</div>\n") # close footer
    f.write("</div>\n") # close container
    f.write("</div>\n") # close content
    f.write("</body>\n")
    f.write("</html>\n")



if __name__ == "__main__":

  plotNames = ["23_04_01_data.png", "23_04_02_data.png", "23_04_03_data.png"]
  if makePage(plotNames):
    print ("Success, html page made for: " + plotNames[1])
