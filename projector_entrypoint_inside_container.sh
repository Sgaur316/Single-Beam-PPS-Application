#!/usr/bin/env/ bash
echo $1

if [ $1 == "app_mode" ]
then
   echo "Running container in application mode"
   python3.6 app.py
else
   echo "Running container in calibration mode"
   python3.6 calibration.py
fi
