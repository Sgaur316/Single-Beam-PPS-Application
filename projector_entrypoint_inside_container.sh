#!/usr/bin/env/ bash
echo $1

if [ $1 == "app_mode" ]
then
   echo "Running container in application mode"
   python app.py
else
   echo "Running container in calibration mode"
   python calibration.py
fi