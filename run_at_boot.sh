#!/bin/bash
clear
HOME=/home/pi/
PYTHONPATH=/home/username/.local/lib/python3.9/site-packages

cd /home/pi/Raspi4/
/usr/bin/python3 /home/pi/MonitorPi/enviroment_CSV.py &
/usr/bin/python3 /home/pi/MonitorPi/CSV2JPG_enviroment.py &
/usr/bin/python3 /home/pi/MonitorPi/GraphFromCSV.py &
