#!/usr/bin/env/ bash
echo $1

if [ $1 == "app_mode" ]
then
   echo "Running container in application mode"
   python3 main.py
else
   echo "Running container in calibration mode"
   python3 main.py cal_mode
fi
