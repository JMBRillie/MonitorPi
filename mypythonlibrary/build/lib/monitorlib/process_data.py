# Finds errors in raw data
# Processes raw data into consistent steps 1 per minute
# Interpolates data in gaps (repeats previous value)

import os

def find_anomilies(filename, valid_chars, error_file):
  with open(filename, "r") as f:
    f.readline()
    lines = f.readlines()
    if ":" in lines[0]:
      lines_col = [line.rstrip().split(",") for line in lines]
      times = [col[0].split(":") for col in lines_col]
      hours = [int(time[0]) for time in times]
      minutes = [int(time[1]) for time in times]
      seconds = [int(time[2]) for time in times]
      for line_num, line in enumerate(lines):
        if any(char not in valid_chars for char in line):
          with open(error_file, "a", newline="") as e:
            e.write(f"[{filename}]->{line_num+2}: {line}\t\t")
            for char in line:
              if char not in valid_chars:
                e.write(f"{char}: {hex(ord(char))}; ")
            e.write("\n")
        if line_num > 1:
          time_err = 0
          if hours[line_num]>hours[line_num -1]:
            pass
          elif hours[line_num]<hours[line_num -1]:
            time_err = 1
          elif minutes[line_num]>minutes[line_num-1]:
            pass
          elif minutes[line_num]<minutes[line_num-1]:
            time_err = 1
          elif seconds[line_num]>seconds[line_num-1]:
            pass
          else:
            time_err = 1

          if time_err:
            with open(error_file, "a", newline="") as e:
              e.write(f"[{filename}]->TIME ERROR: {line_num = }: {line}")
              print(f"[{filename}]->TIME ERROR: {line}")
              print(f"{hours[line_num] = } {hours[line_num -1] = }")
              print(f"{minutes[line_num] = } {minutes[line_num -1] = }")
              print(f"{seconds[line_num] = } {seconds[line_num -1] = }")

def interpolate_data(csvDir, file):
  rawDir = csvDir + "raw/"
  processedDir = csvDir + "days/"
  with open(rawDir + file, "r") as f:
    s_file = processedDir + file
    with open(s_file, "w", newline="") as s:
      s.write(f.readline())
      lines = f.readlines()
      if not ":" in lines[0]:
        return()
      lines_col = [line.rstrip().split(",") for line in lines]
      times = [col[0].split(":") for col in lines_col]
      hours = [time[0] for time in times]
      minutes = [time[1] for time in times]
      seconds = [time[2] for time in times]
      n_lines = len(lines)
      for i in range(n_lines):
        if hours[i] == hours[i-1] and minutes[i] == minutes[i-1]:
          s_line = f"{hours[i]}:{minutes[i]}:00,\
{round((float(lines_col[i][1])+float(lines_col[i-1][1]))/2,1)},\
{round((float(lines_col[i][2])+float(lines_col[i-1][2]))/2,1)},\
{round((float(lines_col[i][3])+float(lines_col[i-1][3]))/2,1)}"
          s.write(f"{s_line}\n")
        else:
          if not( (hours[i] == hours[(i+1)%n_lines] and minutes[i] == minutes[(i+1)%n_lines]) ):
            s_line = f"{hours[i]}:{minutes[i]}:00,\
{lines_col[i][1]},\
{lines_col[i][2]},\
{lines_col[i][3]}"
            s.write(f"{s_line}\n")
  with open(s_file,"r") as s:
    fieldnames = s.readline()
    lines = [line.split(":") for line in s.readlines()]
  with open(s_file, "w", newline="") as s:
    s.write(fieldnames)
    line = 0
    data = lines[0][-1]

    for h in range(24):
      for m in range(60):
        if line < len(lines):
          if (int(lines[line][0]) == h) and (int(lines[line][1]) == m):
            data = lines[line][-1]
            line += 1
        s.write(f"{h:02d}:{m:02d}:{data}")

