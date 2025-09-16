@echo off
cd /d "F:\Python_Automation\DailyUpdate_LinkedIn"

echo Updating Naukri Profile...
python Naukri_DailyUpdate.py

echo.
echo Updating LinkedIn Profile...
python LinkedIn_DailyUpdate.py

echo.
echo All updates completed!
pause
